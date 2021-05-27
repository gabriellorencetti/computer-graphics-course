### Importando as bibliotecas necessárias ###
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

# Variáveis globais
t_x = 0
t_y = 0
s_x = 1
s_y = 1
angulo = 0
height = 720
width = 1280
numVerticesCirculos = 32
day_or_night = False

def criar_matriz():
	matriz = np.array([ 1.0, 0.0, 0.0, 0.0,
						0.0, 1.0, 0.0, 0.0,
						0.0, 0.0, 1.0, 0.0,
						0.0, 0.0, 0.0, 1.0], np.float32)

	return matriz

# Retorna a matriz de translação, dado t_x e t_y
def translacao(t_x, t_y):

	translacao = np.array([ 1.0, 0.0, 0.0, t_x,
							0.0, 1.0, 0.0, t_y,
							0.0, 0.0, 1.0, 0.0,
							0.0, 0.0, 0.0, 1.0], np.float32)

	return translacao

# Retorna a matriz de escala, dado s_x e s_y
def escala(s_x, s_y):

	escala = np.array([ s_x, 0.0, 0.0, 0.0,
						0.0, s_y, 0.0, 0.0,
						0.0, 0.0, 1.0, 0.0,
						0.0, 0.0, 0.0, 1.0], np.float32)

	return escala

# Retorna a matriz de rotação, dado o ângulo
def rotacao(angulo):

	cos_ang = math.cos(angulo)
	sen_ang = math.sin(angulo)

	rotacao = np.array([	cos_ang,	-sen_ang, 	0.0, 0.0,
							sen_ang,	 cos_ang, 	0.0, 0.0,
							0.0,		 0.0, 		1.0, 0.0,
							0.0, 		 0.0,		0.0, 1.0], np.float32)

	return rotacao

# Retorna a multiplicação da matriz A pela matriz B
def multiplica_matriz(matA, matB):
    return ((np.dot(matA.reshape(4,4),matB.reshape(4,4))).reshape(1,16))

def eventos_teclado(window, key, scancode, action, mods):
	
	global t_x, angulo

	if key == 65: angulo += 0.05 #esquerda a
	if key == 68: angulo -= 0.05 #direita d
	if key == 263: t_x -= 0.05 #esquerda
	if key == 262: t_x += 0.05 #direita

def eventos_mouse(window, button, action, mods):

	global s_x, day_or_night

	if action == 1:
		if button == 0:  # esquerdo
			day_or_night = True

		elif button == 1:  # direito
			day_or_night = False

		

def inicializar_janela(height, width):
	glfw.init()
	glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
	window = glfw.create_window(width, height, "Trabalho 1 - Memórias", None, None)
	glfw.make_context_current(window)

	# Captura eventos do teclado e do mouse
	glfw.set_key_callback(window,eventos_teclado)
	glfw.set_mouse_button_callback(window, eventos_mouse)

	return window

# Compila o vertex shader e o fragment shader
def compilar_shader(program, slot, slot_code, type):

	glShaderSource(slot, slot_code)
	glCompileShader(slot)

	if not glGetShaderiv(slot, GL_COMPILE_STATUS):
		error = glGetShaderInfoLog(slot).decode()
		print(error)
		raise RuntimeError("Erro de compilação do " + type + " Shader")

	# atribui os shader objects ao programa
	glAttachShader(program, slot)

def criar_circulo(raio, num_vertices, posX, posY):
    
    vertices_circulo = np.zeros(num_vertices, [("position", np.float32, 2)])
    anguloCirc = 0.0
    
    for i in range(num_vertices):
        anguloCirc += 2*math.pi/num_vertices
        x = posX + math.cos(anguloCirc)*raio/(width/height)
        y = posY + math.sin(anguloCirc)*raio
        vertices_circulo[i] = [x,y]
        
    return vertices_circulo

def criar_pássaro():

	verticesPassaro = np.zeros(17, [("position", np.float32, 2)])

	verticesPassaro['position'] = [
		( 0.0,   +0.74),	# cabeça
		(+0.022, +0.78),
		(+0.026, +0.74),

		(+0.022, +0.78),
		(+0.025, +0.70),
		(+0.065, +0.78),

		(+0.080, +0.81),
		(+0.025, +0.70),
		(+0.182, +0.85),
		(+0.150, +0.722),

		(+0.025, +0.70),
		(+0.150, +0.722),
		(+0.115, +0.64),

		(+0.115, +0.64),
		(+0.122, +0.61),
		(+0.150, +0.722),
		(+0.190,+0.625)
	]

	return verticesPassaro

def criar_catavento():
	
	pe = np.zeros(4, [("position", np.float32, 2)])

	pe['position'] = [
		(-0.715, +0.3),
		(-0.685, +0.3),
		(-0.715, -0.7),
		(-0.685, -0.7)
	]

	pa1 = np.zeros(3, [("position", np.float32, 2)])

	pa1['position'] = [
		(-0.7, +0.3),
		(-0.7, -0.15),
		(-0.55, +0.15)
	]

	pa2 = np.zeros(3, [("position", np.float32, 2)])
	
	pa2['position'] = [
		(-0.7, +0.3),
		(-0.7, +0.75),
		(-0.85, +0.45)
	]

	pa3 = np.zeros(3, [("position", np.float32, 2)])
	pa3['position'] = [
		(-0.70, +0.3),
		(-0.25, +0.3),
		(-0.55, +0.45)
	]

	pa4 = np.zeros(3, [("position", np.float32, 2)])
	pa4['position'] = [
		(-0.70, +0.3),
		(-1.15, +0.3),
		(-0.85, +0.15)
	]

	centro = criar_circulo(0.08, numVerticesCirculos, -0.7, +0.3)

	verticesCatavento = np.concatenate((pe, pa1, pa2, pa3, pa4, centro))

	return verticesCatavento

def rotacao_catavento():
	return (multiplica_matriz(multiplica_matriz(translacao(-0.7, 0.3), rotacao(angulo)), translacao(+0.7, -0.3)))


def criar_casa():

	estruturaCasa = np.zeros(11, [("position", np.float32, 2)])

	estruturaCasa['position'] = [
		(+0.3,  0.0),	# vertice 0 parede
		(+0.7,  0.0),	# vertice 1 parede
		(+0.3, -0.6),	# vertice 2 parede
		(+0.7, -0.6),	# vertice 3 parede

		(+0.3,  0.0),	# vertice 0 telhado
		(+0.7,  0.0),	# vertice 1 telhado
		(+0.5, +0.3),	# vertice 2 telhado

		(+0.45, -0.25),	# vertice 0 porta
		(+0.55, -0.25),	# vertice 1 porta
		(+0.45, -0.60),	# vertice 2 porta
		(+0.55, -0.60)	# vertice 3 porta
	]

	janela = criar_circulo(0.1, numVerticesCirculos, 0.5, 0.05)
	casa = np.concatenate((estruturaCasa, janela))

	return casa

def criar_balao():

	circ_balao = criar_circulo(0.2, numVerticesCirculos, -0.1, 0.2)

	triang_balao = np.zeros(3, [("position", np.float32, 2)])
	
	triang_balao['position'] = [
		(-0.20, +0.11),	# vertice 0 chão
		(-0.00, +0.11),	# vertice 1 chão
		(-0.1, -0.15),	# vertice 2 chão		
	]

	return np.concatenate((triang_balao, circ_balao))


def construir_objetos():
	verticesA = np.zeros(8, [("position", np.float32, 2)])

	verticesA['position'] = [
		(-1.0, -0.2),	# vertice 0 chão
		(-1.0, -1.0),	# vertice 1 chão
		(+1.0, -0.2),	# vertice 2 chão
		(+1.0, -1.0),	# vertice 3 chão

		(-1.0, +1.0),	# vertice 0 céu
		(-1.0, -0.2),	# vertice 1 céu
		(+1.0, +1.0),	# vertice 2 céu
		(+1.0, -0.2)	# vertice 3 céu

	]

	passaro = criar_pássaro()

	sol = criar_circulo(0.2, numVerticesCirculos, 0.8, 0.7)

	catavento = criar_catavento()

	vertices = np.concatenate((verticesA, passaro, sol, catavento, criar_casa(), criar_balao()))

	return vertices

def enviar_dados_gpu(vertices):
	# requisitando um slot de buffer da GPU
	buffer = glGenBuffers(1)

	# tornando-o o padrão
	glBindBuffer(GL_ARRAY_BUFFER, buffer)

	# enviando os dados
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
	glBindBuffer(GL_ARRAY_BUFFER, buffer)

	return buffer


def mostrar_janela(window, program, vertices):

	loc_color = glGetUniformLocation(program, "color")

	glfw.show_window(window)

	while not glfw.window_should_close(window):

		glfw.poll_events()

		glClear(GL_COLOR_BUFFER_BIT)
		glClearColor(1.0, 1.0, 1.0, 1.0)

		# Draw Triangle
		mat_translation = criar_matriz()
		loc = glGetUniformLocation(program, "mat_transformation")
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)

		# Desenhando o chão
		glUniform4f(loc_color, 46/255, 139/255, 87/255, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

		#Desenhando o céu
		if day_or_night == True: glUniform4f(loc_color, 135/255, 206/255, 235/255, 1.0)
		else: glUniform4f(loc_color, 25/255, 25/255, 112/255, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)

		### Desenhando o pássaro ###
		mat_translation = multiplica_matriz(translacao(t_x, t_y), escala(s_x, s_y))
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLES, 8, 3)

		glUniform4f(loc_color, 0.8, 0.8, 0.8, 1.0)
		glDrawArrays(GL_TRIANGLES, 11, 3)
		# asa pássaro
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 14, 4)

		glUniform4f(loc_color, 0.8, 0.8, 0.8, 1.0)
		glDrawArrays(GL_TRIANGLES, 18, 3)
		# asa pássaro
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 21, 4)

		mat_translation = criar_matriz()
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)
		
		### Desenhando o sol ###
		if day_or_night == True: glUniform4f(loc_color, 255/255, 215/255, 0.0, 1.0)
		else: glUniform4f(loc_color, 169/255, 169/255, 169/255, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, 25, numVerticesCirculos)

		### Catavento ###
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 25+numVerticesCirculos, 4)

		glUniformMatrix4fv(loc, 1, GL_TRUE, rotacao_catavento())

		glUniform4f(loc_color, 255/255, 218/255, 185/255, 1.0)
		glDrawArrays(GL_TRIANGLES, 25+numVerticesCirculos+4, 3)

		glUniform4f(loc_color, 238/255, 232/255, 170/255, 1.0)
		glDrawArrays(GL_TRIANGLES, 25+numVerticesCirculos+7, 3)

		glUniform4f(loc_color, 216/255, 191/255, 216/255, 1.0)
		glDrawArrays(GL_TRIANGLES, 25+numVerticesCirculos+10, 3)

		glUniform4f(loc_color, 176/255, 224/255, 230/255, 1.0)
		glDrawArrays(GL_TRIANGLES, 25+numVerticesCirculos+13, 3)

		mat_translation = criar_matriz()
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, 25+numVerticesCirculos+16, numVerticesCirculos)

		######### --- Casa --- #########
		glUniform4f(loc_color, 1.0, 0.98, 0.5, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 25+numVerticesCirculos*2+16, 4)

		#glUniform4f(loc_color, 0.8, 0.8, 0.8, 1.0)
		glDrawArrays(GL_TRIANGLES, 25+numVerticesCirculos*2+20, 3)

		glUniform4f(loc_color, 160/255, 82/255, 45/255, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, 25+numVerticesCirculos*2+23, 4)

		glUniform4f(loc_color, 176/255, 224/255, 230/255, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, 25+numVerticesCirculos*2+27, numVerticesCirculos)


		######### --- Balão --- #########
		glUniform4f(loc_color, 148/255, 0.0, 211/255, 1.0)
		glDrawArrays(GL_TRIANGLES, 25+numVerticesCirculos*3+27, 3)

		#glUniform4f(loc_color, 0.7, 0.2, 0.5, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, 25+numVerticesCirculos*3+30, numVerticesCirculos)
		

		glfw.swap_buffers(window)

	glfw.terminate()

def main():

	window = inicializar_janela(height, width)

	# Requisita slots de programa e shaders para a GPU
	program = glCreateProgram()
	vertex = glCreateShader(GL_VERTEX_SHADER)
	fragment = glCreateShader(GL_FRAGMENT_SHADER)

	vertex_code = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
        """

	fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

	compilar_shader(program, vertex, vertex_code, "Vertex")
	compilar_shader(program, fragment, fragment_code, "Fragment")

	glLinkProgram(program)
	if not glGetProgramiv(program, GL_LINK_STATUS):
		print(glGetProgramInfoLog(program))
		raise RuntimeError('Erro na linkagem')

	glUseProgram(program)

	vertices = construir_objetos()

	buffer = enviar_dados_gpu(vertices)

	stride = vertices.strides[0]
	offset = ctypes.c_void_p(0)

	loc = glGetAttribLocation(program, "position")
	glEnableVertexAttribArray(loc)

	glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

	mostrar_janela(window, program, vertices)

main()
