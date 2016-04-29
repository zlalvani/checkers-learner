var CheckersUI = (function(){

  var canvasId, canvas, width, height, context, sqsz;
  var checkers, pieceMove;

  function init(_canvasId, _props){
    _props = _props || {};
    canvasId = _canvasId;
    width = _props.width || 500;
    height = _props.height || 500;
    canvas = document.getElementById(canvasId);
    canvas.width =  width;
    canvas.height = height;
    context = canvas.getContext('2d');
    sqsz = width / 8;
    canvas.addEventListener('mousedown', startMove);
    canvas.addEventListener('mousemove', mouseMove);
    canvas.addEventListener('mouseup', endMove);
    setInterval(onTick, 1000/30);
    getBoardState();
    pieceMove = {moves:[]};
  }

  function redraw(){
    drawBackground();
    drawCheckers();
  }

  function drawBackground(){
    context.fillStyle = "#fff";
    context.fillRect(0,0,width,height);
    context.fillStyle = "#000";
    for (var x = 0; x < 8; x++){
      for (var y = 0; y < 8; y++){
        if ((x+y)%2 == 0){
          context.fillRect(x * sqsz,y * sqsz,sqsz,sqsz);
        }
      }
    }
  }

  function drawCheckers(){
    for (var i = 0;i < checkers.length;i++){
      drawChecker(checkers[i]);
    }
  }

  function drawChecker(checker){
    context.fillStyle = checker.team == 0 ? "#000": "#f00";
    context.strokeStyle = "#fff";
    context.lineWidth = 5;
    context.beginPath();
    context.arc(checker.x * sqsz + sqsz/2, checker.y *sqsz + sqsz/2, sqsz/2.4, 0, 2 * Math.PI, false);
    context.closePath();
    context.stroke();
    context.fill();
    if (checker.king){
      context.fillStyle = "#fff";
      context.font = "30px Verdana";
      context.textAlign = "center";
      context.fillText("K", checker.x * sqsz + sqsz/2, checker.y * sqsz + sqsz/1.5);
    }
  }

  function getMousePosition(event){
    var bounding = canvas.getBoundingClientRect();
    var x = event.clientX - bounding.left;
    var y = event.clientY - bounding.top;
    return {x:x, y:y};
  }

  function distanceToChecker(checker, point){
    var checker_point = {
      x: checker.x * sqsz + sqsz/2,
      y: checker.y * sqsz + sqsz/2
    };
    return pointDistance(checker_point, point);
  }

  function pointDistance(a, b){
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    return Math.sqrt(dx*dx + dy*dy);
  }

  var grabbing = null;

  function startMove(e){
    var mouse = getMousePosition(e);
    for (var i = 0; i < checkers.length; i++){
      if (distanceToChecker(checkers[i], mouse) < sqsz/2){
        grabbing = i;
        checkers[i].oldx = checkers[i].x;
        checkers[i].oldy = checkers[i].y;
        checkers[i].tx = checkers[i].x;
        checkers[i].ty = checkers[i].y;
        if(pieceMove.moved){
          if(pieceMove.pieceMoved != grabbing){
            console.log("changing")
            pieceMove.moves = [];
            var mc = pieceMove.checker;
            mc.x = pieceMove.starting.coor.xCoor;
            mc.y = pieceMove.starting.coor.yCoor;
            pieceMove.moved = false;
            redraw();
          }
        }
        if(!pieceMove.moved){
          console.log("Setting Starting")
          pieceMove.starting = {coor: {xCoor: checkers[i].x, yCoor: checkers[i].y}};
        }
        pieceMove.pieceMoved = grabbing;
        pieceMove.checker = checkers[i];

        break;
      }
    }
  }

  function mouseMove(e){
    var mouse = getMousePosition(e);
    if (grabbing !== null){
      checkers[grabbing].tx = (mouse.x - sqsz/2) / sqsz;
      checkers[grabbing].ty = (mouse.y - sqsz/2) / sqsz;
      redraw();
    }
  }

  function onTick(){
    if (grabbing !== null){
      var mc = checkers[grabbing];
      if (mc.tx !== undefined){
        mc.x -= (mc.x - mc.tx)/2;
        mc.y -= (mc.y - mc.ty)/2;
      }
      redraw();
    }
  }

  function convertToBoardFmt(){
    var ar = [];
    for (var i = 0;i < 32;i++){
      ar.push(0);
    }
    for (var i = 0;i < checkers.length;i++){
      var index = Math.floor(checkers[i].x/2) + Math.floor(checkers[i].y) * 4;
      ar[index] = (checkers[i].team * 2 - 1) * (checkers[i].king ? 2 : 1);
    }
    return ar;
  }

  function convertToPieceFmt(checkerPiece, xCoor, yCoor){
    var index = Math.floor(xCoor/2)*2 + Math.floor(yCoor) * 4;
    var value = (checkerPiece.team * 2 - 1) * (checkerPiece.king ? 2 : 1);
    xCoor = Math.round(xCoor);
    yCoor = Math.round(yCoor);
    return {coor: [xCoor, yCoor], index: index, value: value}
  }


  function convertFromBoardFmt(boardArray){
    checkers = [];
    for (var i = 0;i < boardArray.length; i++){
      if(boardArray[i] != 0){
        checkers.push({
          x: (i*2)%8 + (Math.floor(1+i/4)%2),
          y: Math.floor(i/4),
          king : Math.abs(boardArray[i]) > 1,
          team: boardArray[i] > 0
        });
      }
    }
  }


  function endMove(e){
    var mouse = getMousePosition(e);
    if (grabbing !== null){
      var mc = checkers[grabbing];
      mc.x = Math.round(mouse.x/sqsz - .5);
      mc.y = Math.round(mouse.y/sqsz - .5);
      var movePiece = convertToPieceFmt(mc, mc.oldx, mc.oldy);
      var movePositions = [convertToPieceFmt(mc, mc.x, mc.y)];
      // Record Move in list for sending
      pieceMove.moved = true;
      pieceMove.moves.push({coor: {xCoor: mc.x, yCoor: mc.y}});
      grabbing = null;
      redraw();
    }
  }

  function getBoard(){
    return convertToBoardFmt();
  }

  function getBoardState(){
    $.ajax({
        url: 'http://localhost:8080/api/getBoard',
        type: 'GET',
        success: function (data) {
            convertFromBoardFmt(data.board)
            redraw();
        },
        error: function (xhr, status, error) {
            console.log('Error: ' + error.message);
        },
    });
  }

  function load(board){
    checkers = [];
    for (var i = 0;i < board.length;i++){
      if (board[i] != 0){
        var king = Math.abs(board[i]) > 1;
        var team = (Math.sign(board[i]) + 1)/2;
        var x = ((i%4) * 2) + (Math.floor(1+i/4)%2);
        var y = Math.floor(i/4);
        checkers.push({
          x: x,
          y: y,
          team: team,
          king: king
        });
      }
    }
    redraw();
  }

  function validate(board, movePiece, movePositions, cb){
    $.ajax({
        url: 'http://localhost:8080/api/verify',
        data: {board: board, movePiece: movePiece, movePositions: movePositions},
        type: 'POST',
        success: function (data) {
            cb(data.works);
        },
        error: function (xhr, status, error) {
            console.log('Error: ' + error.message);
            cb(false);
        },
    });
  }

  function AIMove(){
    $.ajax({
        url: 'http://localhost:8080/api/getAIMove',
        type: 'GET',
        success: function (data) {
            convertFromBoardFmt(data.board)
            redraw();
        },
        error: function (xhr, status, error) {
            console.log('Error: ' + error.message);
        },
    });
  }

  function makeMove(){
    pieceMove.moved = false;
    self.validate(convertToBoardFmt(), pieceMove.starting, pieceMove.moves, (valid)=>{
      if(!valid){
        var mc = pieceMove.checker;
        mc.x = pieceMove.starting.coor.xCoor;
        mc.y = pieceMove.starting.coor.yCoor
      }
      grabbing = null;
      redraw();
      if(valid){
        AIMove();
      }
    });
  }

  var self = {
    init: init,
    load: load,
    getBoard: getBoard,
    getBoardState: getBoardState,
    makeMove: makeMove,
    validate: validate,
    AIMove: AIMove
  };
  return self;
})();
