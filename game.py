import time
from turtle import Turtle
from turtle import Screen
import random
from network import Network


run = True


class Game:
	def __init__(self):
		self.screen = Screen()
		self.screen.tracer(0)
		self.screen.setup(width=800, height=600)
		self.screen.bgcolor("black")
		self.screen.title("Pong_v2")
		self.player1 = Paddle((-350, 0))
		self.player2 = Paddle((350, 0))
		self.players = [self.player1, self.player2]
		self.ball = Ball((0, 0))
		self.scoreboard = Scoreboard()
		self.screen.update()
		self.net = Network()
		self.id = self.net.id

	@staticmethod
	def game_quit():
		global run
		run = False

	def run(self):
		global run
		self.screen.listen()
		current_paddle = self.players[int(self.id)] # To be added from Network
		run = True
		while True:
			self.screen.update()
			self.screen.onkey(current_paddle.go_up, "Up")
			self.screen.onkey(current_paddle.go_down, "Down")
			self.screen.onkey(self.game_quit, "q")
			if self.id == "0":
				self.game_logic()
				data = {"id": self.id,
						"0": self.player1.ycor(),
						"ball": (self.ball.xcor(), self.ball.ycor())}
				reply = self.net.send(data)
				player2_ypos = reply.get("1")
				self.player2.goto((350, player2_ypos))
			if self.id == "1":
				data = {"id": self.id,
						"1": self.player1.ycor()}
				reply = self.net.send(data)
				player1_ypos = reply.get("0")
				ball_pos = reply.get("ball")
				self.player1.goto((-350, player1_ypos))
				self.ball.goto(ball_pos)

	def game_logic(self):
		self.ball.move()
		# Detect wall collision
		if self.ball.ycor() > 290 or self.ball.ycor() < -290:
			self.ball.y_bounce()
		# Detect r_paddle collision
		if self.ball.distance(self.player2) < 50 and self.ball.xcor() > 340:
			self.ball.x_bounce()
		# Detect l_paddle collision
		if self.ball.distance(self.player1) < 50 and self.ball.xcor() < -340:
			self.ball.x_bounce()
		# Detect right miss
		if self.ball.xcor() > 390:
			time.sleep(0.5)
			self.ball.new_angle("right")
			self.ball.ball_speed = 4
			self.scoreboard.l_point()
		# Detect left miss
		if self.ball.xcor() < -390:
			time.sleep(0.5)
			self.ball.new_angle("left")
			self.ball.ball_speed = 4
			self.scoreboard.r_point()
	def send_data(self):
		"""
		Sending data using Network class
		:return:
		"""

	@staticmethod
	def receive_data():
		"""
		Receiving data from server
		:return:
		"""


class Scoreboard(Turtle):
	def __init__(self):
		super().__init__()
		self.color("white")
		self.penup()
		self.hideturtle()
		self.l_score = 0
		self.r_score = 0
		self.scoreboard_update()

	def scoreboard_update(self):
		self.clear()
		self.goto(-100, 200)
		self.write(self.l_score, align="center", font=("Courier", 80, "normal"))
		self.goto(100, 200)
		self.write(self.r_score, align="center", font=("Courier", 80, "normal"))

	def l_point(self):
		self.l_score += 1
		self.scoreboard_update()

	def r_point(self):
		self.r_score += 1
		self.scoreboard_update()


class Ball(Turtle):
	def __init__(self, position):
		super().__init__()
		self.shape("circle")
		self.color("white")
		self.penup()
		self.setpos(position)
		self.right_move = random.randint(0, 180)
		self.left_move = random.randint(180, 360)
		self.setheading(self.right_move)
		self.ball_speed = 4

	def new_angle(self, side):
		right_list = [(0, 60), (300, 360)]
		right = random.choice(right_list)
		self.right_move = random.randint(right[0], right[1])
		self.left_move = random.randint(120, 240)
		self.setpos(0, 0)
		if side == "left":
			self.setheading(self.right_move)
		elif side == "right":
			self.setheading(self.left_move)

	def move(self):
		self.forward(self.ball_speed)

	def y_bounce(self):
		angle = self.heading()
		new_angle = 360 - angle
		self.setheading(new_angle)

	def x_bounce(self):
		angle = self.heading()
		new_angle = 180 - angle
		self.setheading(new_angle)
		self.ball_speed += 0.5


class Paddle(Turtle):
	def __init__(self, position):
		super().__init__()
		self.shape("square")
		self.color("white")
		self.penup()
		self.setpos(position)
		self.shapesize(stretch_wid=1, stretch_len=5)
		self.setheading(90)

	def go_up(self):
		self.forward(20)

	def go_down(self):
		self.back(20)
