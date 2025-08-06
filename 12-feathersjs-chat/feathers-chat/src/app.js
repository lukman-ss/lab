const feathers = require('@feathersjs/feathers');
const express  = require('@feathersjs/express');
const socketio = require('@feathersjs/socketio');

const app = express(feathers());

// Parsers & REST
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.configure(express.rest());

// Real-time via Socket.IO (this sets up app.io)
app.configure(socketio());

// In-memory stores
app.set('rooms', new Map());
app.set('messagesMap', {});

// HTTP POST /room  → create a room
app.post('/room', (req, res) => {
  const rooms = app.get('rooms');
  const { room_id } = req.body;

  if (!room_id) {
    return res.status(400).json({ error: 'room_id is required' });
  }
  if (rooms.has(room_id)) {
    return res.status(409).json({ error: 'room already exists' });
  }

  rooms.set(room_id, new Set());
  app.get('messagesMap')[room_id] = [];
  return res.status(201).json({ status: 'room created', room_id });
});

// HTTP POST /send  → send a message to a room
app.post('/send', (req, res) => {
  const rooms       = app.get('rooms');
  const messagesMap = app.get('messagesMap');
  const io          = app.io;
  const { room_id, message } = req.body;

  if (!room_id || !message) {
    return res.status(400).json({ error: 'room_id and message are required' });
  }
  if (!rooms.has(room_id)) {
    return res.status(404).json({ error: 'room not found' });
  }

  messagesMap[room_id].push(message);
  io.to(room_id).emit('newMessage', { room_id, message });
  return res.json({ status: 'sent' });
});

module.exports = app;
