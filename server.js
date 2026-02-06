const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http, {
  cors: { origin: "*" }
});

// Oyuncuların listesini tutar
let players = {};

io.on('connection', (socket) => {
  console.log('Bir oyuncu bağlandı: ' + socket.id);
  
  // Yeni oyuncuyu oluştur
  players[socket.id] = { x: 0, y: 0.5, z: 0 };
  
  // Mevcut oyuncuları yeni gelene bildir
  socket.emit('currentPlayers', players);
  
  // Yeni oyuncuyu diğerlerine bildir
  socket.broadcast.emit('newPlayer', { id: socket.id, pos: players[socket.id] });

  // Hareket verisi geldiğinde
  socket.on('playerMovement', (movementData) => {
    players[socket.id] = movementData;
    socket.broadcast.emit('playerMoved', { id: socket.id, pos: players[socket.id] });
  });

  // Bağlantı kesildiğinde
  socket.on('disconnect', () => {
    delete players[socket.id];
    io.emit('playerDisconnected', socket.id);
  });
});

const PORT = process.env.PORT || 3000;
http.listen(PORT, () => {
  console.log(`Sunucu ${PORT} portunda çalışıyor.`);
});