module.exports = function (app) {
  const rooms       = app.get('rooms');
  const messagesMap = app.get('messagesMap');
  const io          = app.io;

  io.on('connection', socket => {
    // join or create a room
    socket.on('joinRoom', ({ room_id }) => {
      if (!rooms.has(room_id)) {
        rooms.set(room_id, new Set());
        messagesMap[room_id] = [];
      }
      socket.join(room_id);
      rooms.get(room_id).add(socket.id);
      socket.emit('joinedRoom', { room_id });
    });

    // list all rooms
    socket.on('listRoom', () => {
      socket.emit('roomList', Array.from(rooms.keys()));
    });

    // list chat history for one room
    socket.on('listChat', ({ room_id }) => {
      const history = messagesMap[room_id] || [];
      socket.emit('chatList', history);
    });

    // send a new message over WS
    socket.on('sendMessage', ({ room_id, message }) => {
      if (rooms.has(room_id)) {
        messagesMap[room_id].push(message);
        io.to(room_id).emit('newMessage', { room_id, message });
      } else {
        socket.emit('error', 'room not found');
      }
    });

    // cleanup on disconnect
    socket.on('disconnect', () => {
      rooms.forEach(members => members.delete(socket.id));
    });
  });
};
