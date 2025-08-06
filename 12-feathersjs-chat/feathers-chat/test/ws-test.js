// ws-test.js
const { io } = require("socket.io-client");

// Adjust URL/port if needed
const SOCKET_URL = "http://localhost:3030";
const OPTIONS    = {
  path: "/socket.io",
  transports: ["websocket"],
};

const socket = io(SOCKET_URL, OPTIONS);

socket.on("connect", () => {
  console.log("✅ WS connected, id =", socket.id);

  // 1) List rooms
  socket.emit("listRoom");
});

socket.on("roomList", (rooms) => {
  console.log("📦 roomList:", rooms);

  // 2) Pick the first room (or a known one) to list chat
  const room = rooms[0] || "room1";
  socket.emit("listChat", { room_id: room });
});

socket.on("chatList", (msgs) => {
  console.log("💬 chatList:", msgs);

  // All tests done—keeping the socket open so you can
  // manually emit sendMessage or joinRoom if you like.
  console.log("🟢 Tests complete, socket remains open for further manual tests.");
});

socket.on("connect_error", (err) => {
  console.error("❌ Connection error:", err.message);
});

socket.on("error", (err) => {
  console.error("⚠️ Server error event:", err);
});

socket.on("disconnect", (reason) => {
  console.log("🔌 Disconnected:", reason);
});
