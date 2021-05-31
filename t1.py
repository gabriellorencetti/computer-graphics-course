################################################################################

# Trabalho 1

### Feito por:
#### Gabriel Garcia Lorencetti - NUSP 10691891
#### Caio Augusto Duarte Basso - NUSP 10801173

#### A ideia é criar um cenário simples, que traga memórias da vida do interior
#### e da infância.

### Funcionamento:
#### - as teclas 'a' e 'd' rotacionam o lindo catavento colorido;
#### - as teclas 'w' e 's' aumentam e diminuem o tamanho do balão roxo;
#### - as setas para esquerda e direita movimentam o belo pássaro branco
####   que sobrevoa os céus;
#### - os botões direito e esquerdo do mouse alteram entre dia e noite!

### Divirta-se e sinta-se em casa nesse cenário!

################################################################################

# para compilar, basta digitar no terminal: $ pyhon3 t1.py

######### ----- Importando as bibliotecas necessárias ----- ############
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

########## ----- Matrizes de transformação ----- ##########

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


# Retorna uma matriz que não realiza nenhuma alteração
def criar_matriz():
	matriz = np.array([ 1.0, 0.0, 0.0, 0.0,
						0.0, 1.0, 0.0, 0.0,
						0.0, 0.0, 1.0, 0.0,
						0.0, 0.0, 0.0, 1.0], np.float32)
	return matriz


# Retorna uma matriz de translação em t_x e t_y e respeitando o aspect ratio
# -> Utilizado para a rotação do catavento
def translacao_AR1(t_x, t_y):
	grr = escala = np.array([ 	1/WIDTH, 	0.0, 		0.0, (t_x/WIDTH)+t_x,
								0.0, 		1/HEIGHT, 	0.0, (t_y/HEIGHT)+t_y,
								0.0, 		0.0, 		1.0, 0.0,
								0.0, 		0.0, 		0.0, 1.0], np.float32)
	return grr


# Retorna uma matriz de translação em t_x e t_y e respeitando o aspect ratio
# -> Utilizado para a rotação do catavento
def translacao_AR2(t_x, t_y):
	grr = escala = np.array([ 	WIDTH, 	0.0, 	0.0, (WIDTH*t_x)+t_x,
								0.0, 	HEIGHT, 0.0, (HEIGHT*t_y)+t_y,
								0.0, 	0.0, 	1.0, 0.0,
								0.0, 	0.0, 	0.0, 1.0], np.float32)
	return grr


# Retorna a multiplicação da matriz A pela matriz B
def multiplica_matriz(matA, matB):
    return ((np.dot(matA.reshape(4,4),matB.reshape(4,4))).reshape(1,16))


# Retorna a matriz de rotação do catavento, com ponto de referência
# e respeitando o aspect ratio
def rotacao_catavento():	
	return (multiplica_matriz(multiplica_matriz(translacao_AR1(-0.7, 0.3), 
				rotacao(angulo)), translacao_AR2(+0.7, -0.3)))


# Retorna a matriz de rotação do balão, com ponto de referência
def escala_balao():
	trans = translacao(-0.1, -0.15)
	esc = escala(s, s)
	trans2 = translacao(+0.1, +0.15)	
	return multiplica_matriz(multiplica_matriz(trans, esc), trans2)


# Retorna a matriz de translação do pássaro, realizando também
# o espelhamento de acordo com a tecla pressionada
def translacao_passaro():

	trans = translacao(t_x, t_y)

	if invertPass == True: esc = escala(-1, 1)
	elif invertPass == False: esc = escala(1, 1)

	return multiplica_matriz(trans, esc)


########## ----- Variáveis globais ----- ##########

# Defines tamanho primitivas
CIRC = 32
QUAD = 4
TRI = 3

# Defines altura e comprimento da janela
HEIGHT = 720
WIDTH = 1280

# Variáveis controladas pelo teclado
t_x = 0
t_y = 0
s = 1
angulo = 0

# Variáveis de controle de dia/noite e inversão do pássaro
day_or_night = False
invertPass = False

# Variáveis de controle dos objetos
posAtual = 0
objetos = [0]

# Classe Objeto, que armazena a posição no vetor vertice e o tipo
class Objeto:
    def __init__(self, posInicial, tipo):
        self.posInicial = posInicial
        self.tipo = tipo

# Cria o Objeto e o adiciona em uma lista
def add_objeto(tipo):
    global posAtual
    o = Objeto(posAtual, tipo)
    posAtual += tipo
    objetos.append(o)

###################################################


########## ----- Captura de eventos teclado/mouse ----- ##########

# Captura eventos do teclado
def eventos_teclado(window, key, scancode, action, mods):
	
	global t_x, angulo, s, invertPass

	if key == 65: angulo += 0.05 #esquerda a
	if key == 68: angulo -= 0.05 #direita d
	if key == 263 and t_x > -0.9:
		t_x -= 0.01 #esquerda
		invertPass = False
	if key == 262 and t_x < 0.5:
		t_x += 0.01 #direita
		invertPass = True
	if key == 87 and s <= 1.4:
		s += 0.005 # escala+
	if key == 83 and s >= 0.5:
		s -= 0.005


# Captura eventos do mouse
def eventos_mouse(window, button, action, mods):

	global s_x, day_or_night

	if action == 1:
		if button == 0:  # esquerdo
			day_or_night = True

		elif button == 1:  # direito
			day_or_night = False

########################################################

# Inicializa a janela
def inicializar_janela(HEIGHT, WIDTH):
	glfw.init()
	glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
	window = glfw.create_window(WIDTH, HEIGHT, "Trabalho 1 - Memórias", None, None)
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


########## ----- Criação dos objetos ----- ##########

# Dado o raio, número de vértices e a posição X e Y, retorna um vetor
# contendo os vértices do círculo
def criar_circulo(raio, num_vertices, posX, posY):
    
    vertices_circulo = np.zeros(num_vertices, [("position", np.float32, 2)])
    anguloCirc = 0.0
    
    for i in range(num_vertices):
        anguloCirc += 2*math.pi/num_vertices
        x = posX + math.cos(anguloCirc)*raio/(WIDTH/HEIGHT)
        y = posY + math.sin(anguloCirc)*raio
        vertices_circulo[i] = [x,y]
        
    return vertices_circulo


# Retorna os vértices do pássaro
def criar_pássaro():

	verticesPassaro = np.zeros(17, [("position", np.float32, 2)])

	verticesPassaro['position'] = [
		( 0.0,   +0.74),
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
		(+0.190, +0.625)
	]

	add_objeto(TRI)
	add_objeto(TRI)
	add_objeto(QUAD)
	add_objeto(TRI)
	add_objeto(QUAD)


	return verticesPassaro


# Retorna os vértices do catavento
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
		(-0.40, +0.3),
		(-0.60, +0.50)
	]

	pa4 = np.zeros(3, [("position", np.float32, 2)])
	pa4['position'] = [
		(-0.70, +0.3),
		(-1.00, +0.3),
		(-0.80, +0.1)
	]

	centro = criar_circulo(0.08, CIRC, -0.7, +0.3)

	add_objeto(QUAD)
	add_objeto(TRI)
	add_objeto(TRI)
	add_objeto(TRI)
	add_objeto(TRI)
	add_objeto(CIRC)

	verticesCatavento = np.concatenate((pe, pa1, pa2, pa3, pa4, centro))

	return verticesCatavento


# Retorna os vértices da casa
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

	janela = criar_circulo(0.08, CIRC, 0.5, -0.10)

	add_objeto(QUAD)
	add_objeto(TRI)
	add_objeto(QUAD)
	add_objeto(CIRC)

	casa = np.concatenate((estruturaCasa, janela))

	return casa


# Retorna os vértices do balão
def criar_balao():

	circ_balao = criar_circulo(0.2, CIRC, -0.1, 0.2)

	triang_balao = np.zeros(3, [("position", np.float32, 2)])
	
	triang_balao['position'] = [
		(-0.20, +0.11),
		(-0.00, +0.11),
		(-0.1, -0.15)	
	]

	add_objeto(TRI)
	add_objeto(CIRC)

	caixa = np.zeros(4, [("position", np.float32, 2)])
	
	caixa['position'] = [
		(-0.15, -0.15),
		(-0.05, -0.15),
		(-0.15, -0.30),
		(-0.05, -0.30)
	]

	add_objeto(QUAD)

	return np.concatenate((triang_balao, circ_balao, caixa))


# Retorna os vértices do lago e do peixe
def criar_lago():

	dir = criar_circulo(0.3, CIRC, -0.15, -0.8)
	esq = criar_circulo(0.3, CIRC, -0.35, -0.8)

	add_objeto(CIRC)
	add_objeto(CIRC)

	peixe = np.zeros(9, [("position", np.float32, 2)])

	peixe['position'] = [
		(-0.34, -0.66),
		(-0.34, -0.74),
		(-0.30, -0.70),

		(-0.30, -0.70),
		(-0.22, -0.62),
		(-0.22, -0.78),

		(-0.22, -0.62),
		(-0.22, -0.78),
		(-0.16, -0.70)
	]

	add_objeto(TRI)
	add_objeto(TRI)
	add_objeto(TRI)


	return np.concatenate((dir, esq, peixe))


# Retorna os vértices do céu e do chão
def criar_background():

	verticesBack = np.zeros(8, [("position", np.float32, 2)])

	verticesBack['position'] = [
		(-1.0, -0.2),	# vertice 0 chão
		(-1.0, -1.0),	# vertice 1 chão
		(+1.0, -0.2),	# vertice 2 chão
		(+1.0, -1.0),	# vertice 3 chão

		(-1.0, +1.0),	# vertice 0 céu
		(-1.0, -0.2),	# vertice 1 céu
		(+1.0, +1.0),	# vertice 2 céu
		(+1.0, -0.2)	# vertice 3 céu
	]

	add_objeto(QUAD)
	add_objeto(QUAD)

	return verticesBack

def criar_sol():
	add_objeto(CIRC)
	return criar_circulo(0.2, CIRC, 0.8, 0.7)

# Concatena todos os vértices de todos os objetos, para enviar à GPU
def construir_objetos():
	return np.concatenate((	criar_background(), criar_pássaro(), criar_sol(), 
							criar_catavento(), criar_casa(), criar_balao(),
							criar_lago()
							))

######################################################


# Envia todos os dados necessários para a construção dos objetos à CPU
def enviar_dados_gpu(vertices):
	# requisitando um slot de buffer da GPU
	buffer = glGenBuffers(1)

	# tornando-o o padrão
	glBindBuffer(GL_ARRAY_BUFFER, buffer)

	# enviando os dados
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
	glBindBuffer(GL_ARRAY_BUFFER, buffer)

	return buffer

def convRGB(R, G, B):
	return R/255, G/255, B/255

# Mostra a janela e os objetos construídos, com suas transformações
def mostrar_janela(window, program, vertices):

	loc_color = glGetUniformLocation(program, "color")

	glfw.show_window(window)

	while not glfw.window_should_close(window):

		glfw.poll_events()

		glClear(GL_COLOR_BUFFER_BIT)
		glClearColor(1.0, 1.0, 1.0, 1.0)

		mat_translation = criar_matriz()
		loc = glGetUniformLocation(program, "mat_transformation")
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)

		
		###### Desenhando o chão ######
		R, G, B = convRGB(46,139,87)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[1].posInicial, objetos[1].tipo)


		###### Desenhando o céu ######
		if day_or_night == False: R, G, B = convRGB(135,206,235)
		else: R, G, B = convRGB(25,25,112)

		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[2].posInicial, objetos[2].tipo)


		###### Desenhando o pássaro ######
		glUniformMatrix4fv(loc, 1, GL_TRUE, translacao_passaro())
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[3].posInicial, objetos[3].tipo)

		glUniform4f(loc_color, 0.8, 0.8, 0.8, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[4].posInicial, objetos[4].tipo)

		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[5].posInicial, objetos[5].tipo)

		glUniform4f(loc_color, 0.8, 0.8, 0.8, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[6].posInicial, objetos[6].tipo)

		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[7].posInicial, objetos[7].tipo)

		# colocando a matriz neutra para não aplicar a translacao_passaro()
		# aos proximos objetos
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)
		

		###### Desenhando o sol ######
		if day_or_night == False: R, G, B = convRGB(255, 215, 0)
		else: R, G, B = convRGB(169, 169, 169)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, objetos[8].posInicial, objetos[8].tipo)


		###### Catavento ######
		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[9].posInicial, objetos[9].tipo)

		glUniformMatrix4fv(loc, 1, GL_TRUE, rotacao_catavento())
		
		R, G, B = convRGB(255, 218, 155)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[10].posInicial, objetos[10].tipo)

		R, G, B = convRGB(238, 232, 100)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[11].posInicial, objetos[11].tipo)

		R, G, B = convRGB(216, 191, 256)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[12].posInicial, objetos[12].tipo)

		R, G, B = convRGB(40, 180, 250)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[13].posInicial, objetos[13].tipo)


		# colocando a matriz neutra para não aplicar a rotacao_catavento()
		# aos proximos objetos
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)

		glUniform4f(loc_color, 1.0, 1.0, 1.0, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, objetos[14].posInicial, objetos[14].tipo)


		######### --- Casa --- #########
		R, G, B = convRGB(255, 250, 128)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[15].posInicial, objetos[15].tipo)

		R, G, B = convRGB(250, 86, 26)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[16].posInicial, objetos[16].tipo)

		R, G, B = convRGB(160, 82, 45)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[17].posInicial, objetos[17].tipo)

		R, G, B = convRGB(186, 234, 230)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, objetos[18].posInicial, objetos[18].tipo)


		######### --- Balão --- #########
		glUniformMatrix4fv(loc, 1, GL_TRUE, escala_balao())

		R, G, B = convRGB(148, 0, 211)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[19].posInicial, objetos[19].tipo)

		glDrawArrays(GL_TRIANGLE_FAN, objetos[20].posInicial, objetos[20].tipo)

		R, G, B = convRGB(160, 82, 45)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_STRIP, objetos[21].posInicial, objetos[21].tipo)		
		

		# colocando a matriz neutra para não aplicar a escala_balao()
		# aos proximos objetos
		glUniformMatrix4fv(loc, 1, GL_TRUE, mat_translation)


		######### --- Lago --- #########
		R, G, B = convRGB(59, 179, 208)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLE_FAN, objetos[22].posInicial, objetos[22].tipo)
		glDrawArrays(GL_TRIANGLE_FAN, objetos[23].posInicial, objetos[23].tipo)

		R, G, B = convRGB(255, 140, 0)
		glUniform4f(loc_color, R, G, B, 1.0)
		glUniform4f(loc_color, 1.0, 140/255, 0.0, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[24].posInicial, objetos[24].tipo)

		R, G, B = convRGB(0, 0, 128)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[25].posInicial, objetos[25].tipo)

		R, G, B = convRGB(255, 140, 0)
		glUniform4f(loc_color, R, G, B, 1.0)
		glDrawArrays(GL_TRIANGLES, objetos[26].posInicial, objetos[26].tipo)
		

		glfw.swap_buffers(window)

	glfw.terminate()


def main():

	window = inicializar_janela(HEIGHT, WIDTH)

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