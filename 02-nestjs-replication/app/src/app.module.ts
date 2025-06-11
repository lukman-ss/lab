import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';

import { Message } from './message.entity';
import { MessagesController } from './messages.controller';
import { MessagesService } from './messages.service';
import { slaveDataSource } from './database.providers';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      ignoreEnvFile: false, // set true kalau ENV dari docker-compose
    }),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DATABASE_HOST,
      port: parseInt(process.env.DATABASE_PORT || '5432', 10),
      username: process.env.DATABASE_USER,
      password: process.env.DATABASE_PASSWORD,
      database: process.env.DATABASE_NAME,
      synchronize: true,
      autoLoadEntities: true,
    }),
    TypeOrmModule.forFeature([Message]),
  ],
  controllers: [MessagesController],
  providers: [
    MessagesService,
    {
      provide: 'SLAVE_DATA_SOURCE',
      useFactory: async () => {
        if (!slaveDataSource.isInitialized) {
          await slaveDataSource.initialize();
        }
        return slaveDataSource;
      },
    },
  ],
})
export class AppModule {}
