import { Controller, Get, Post, Body } from '@nestjs/common';
import { MessagesService } from './messages.service';

@Controller('messages')
export class MessagesController {
  constructor(private readonly service: MessagesService) {}

  @Get()
  async getAll() {
    return this.service.findAll();
  }

  @Post()
  async create(@Body('text') text: string) {
    return this.service.create(text);
  }
}
