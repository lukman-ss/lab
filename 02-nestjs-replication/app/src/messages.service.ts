import { Injectable, Inject } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Message } from './message.entity';
import { Repository, DataSource } from 'typeorm';

@Injectable()
export class MessagesService {
  constructor(
    @InjectRepository(Message)
    private readonly messageRepo: Repository<Message>,

    @Inject('SLAVE_DATA_SOURCE')
    private readonly slaveDataSource: DataSource,
  ) {}

  async findAll(): Promise<Message[]> {
    const slaveRepo = this.slaveDataSource.getRepository(Message);
    return slaveRepo.find(); // Read from slave
  }

  async create(text: string): Promise<Message> {
    const message = this.messageRepo.create({ text });
    return this.messageRepo.save(message); // Write to master
  }
}
