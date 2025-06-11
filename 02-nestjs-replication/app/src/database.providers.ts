import { DataSource } from 'typeorm';
import { Message } from './message.entity';

export const masterDataSource = new DataSource({
  type: 'postgres',
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT || '5432', 10),
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  synchronize: true,
  entities: [Message],
});

export const slaveDataSource = new DataSource({
  type: 'postgres',
  host: process.env.SLAVE_DB_HOST,
  port: parseInt(process.env.SLAVE_DB_PORT || '5432', 10),
  username: process.env.SLAVE_DB_USER,
  password: process.env.SLAVE_DB_PASSWORD,
  database: process.env.SLAVE_DB_NAME,
  synchronize: false,
  entities: [Message],
});
