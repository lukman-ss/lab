// src/index.js
const http       = require('http');
const { Server } = require('socket.io');
const app        = require('./app');
const channels   = require('./channels');

const PORT = process.env.PORT || 3030;

// Create HTTP server from the Express/Feathers app
const server = http.createServer(app);

// Attach Socket.IO
const io = new Server(server, {
  cors: { origin: '*' },
  path: '/socket.io'
});
app.io = io;

// Wire up real-time channels
channels(app);

// Start listening
server.listen(PORT, () => {
  console.log(`🚀 Server listening on http://localhost:${PORT}`);
  console.log(`🟢 WebSocket via Socket.IO at ws://localhost:${PORT}/socket.io`);
});
