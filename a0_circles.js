// Adapted from https://readyletsgo.github.io/

var currentMin = 0;
var MAX_CIRCLE_SIZE = 100.0;
var MAX_HOURS = 24;
var MAX_MINUTES = 60;
var MAX_SECONDS = 60;


var sizePerHour = MAX_CIRCLE_SIZE/MAX_HOURS;
var sizePerMinute = MAX_CIRCLE_SIZE/MAX_MINUTES;
var sizePerSecond = MAX_CIRCLE_SIZE/MAX_SECONDS;


var HEIGHT = MAX_CIRCLE_SIZE + 30;
var OBJECT_SEPARATION = 30;
var STARTING_X = MAX_CIRCLE_SIZE + OBJECT_SEPARATION;
var CANVAS_WIDTH = 4 * (MAX_CIRCLE_SIZE + OBJECT_SEPARATION) + 20;
var CANVAS_HEIGHT = HEIGHT + MAX_CIRCLE_SIZE;
//this gets called only once in the very beginning
function setup() {
  createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
}

//this gets called every frame (about 60 frames per second)
function draw() {
  var h = hour();
  var min = minute();
  var sec = second();
  background(103, 245, 143);
  // background(200);

  noStroke();

  circle(STARTING_X, HEIGHT, MAX_CIRCLE_SIZE);
  fill(185, 250, 204);
  circle(STARTING_X, HEIGHT, sizePerHour * h);
  fill(160, 250, 186);

  circle(STARTING_X + OBJECT_SEPARATION + MAX_CIRCLE_SIZE, HEIGHT, MAX_CIRCLE_SIZE);
  fill(185, 250, 204);
  circle(STARTING_X + OBJECT_SEPARATION + MAX_CIRCLE_SIZE, HEIGHT, sizePerMinute * min);
  fill(160, 250, 186);

  circle(STARTING_X + 2 * (OBJECT_SEPARATION + MAX_CIRCLE_SIZE), HEIGHT, MAX_CIRCLE_SIZE);
  fill(185, 250, 204);
  circle(STARTING_X + 2 * (OBJECT_SEPARATION + MAX_CIRCLE_SIZE), HEIGHT, sizePerSecond * sec);
  fill(160, 250, 186);

  if (currentMin != min)
  {
    currentMin = min;
    print(currentMin)
  }
}



// colors:
  // green: 82, 252, 3

  // blue: 3, 248, 252

  // purple: 211, 3, 252
  // white: 255, 255, 255
  // Greens:
    // lightest: 185, 250, 204
    // darker: 160, 250, 186
    // darker: 103, 245, 143
