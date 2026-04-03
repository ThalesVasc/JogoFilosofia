import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
import sys
import os

# Função para encontrar o caminho correto dos arquivos (funciona no .exe e no código fonte)
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class Aplicacao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Exibir imagem")
        self.janela.geometry("800x600")
        
        # Carregar imagem original (usando resource_path)
        caminho_imagem = resource_path(os.path.join("imagens", "rose-3061486_640.png"))
        self.imagem_original = Image.open(caminho_imagem)
        
        # Definir tamanho da imagem
        self.tamanho_imagem = (400, 400)
        self.imagem_redimensionada = self.imagem_original.resize(self.tamanho_imagem, Image.Resampling.LANCZOS)
        
        # Configuração do grid (3x3 = 9 blocos)
        self.grid_size = 3
        self.blocos_revelados = [False] * (self.grid_size * self.grid_size)
        
        # Flag para controlar se a imagem está nítida
        self.imagem_nitida = False
        
        # Armazenar versões embaçadas e nítidas dos blocos
        self.blocos_nitidos = []
        self.blocos_embacados = []
        
        # Configuração: cada pergunta revela um ou mais blocos EMBACADOS
        self.revelacao_por_pergunta = [
            [6],                    # Pergunta 1: revela bloco inferior esquerdo (embaçado)
            [8],                    # Pergunta 2: revela bloco inferior direito (embaçado)
            [7],                    # Pergunta 3: revela bloco inferior meio (embaçado)
            [3, 5, 4],             # Pergunta 4: revela meio esquerdo, meio direito e centro (embaçados)
            [0, 1, 2]              # Pergunta 5: revela todos os blocos superiores e TORNA TUDO NÍTIDO!
        ]
        
        # Configuração das reflexões e respostas (5 perguntas)
        self.reflexoes = [
            {"pergunta": "Reflexão1", "resposta": "resposta1"},
            {"pergunta": "Reflexão2", "resposta": "resposta2"},
            {"pergunta": "Reflexão3", "resposta": "resposta3"},
            {"pergunta": "Reflexão4", "resposta": "resposta4"},
            {"pergunta": "Reflexão5", "resposta": "resposta5"}
        ]
        
        self.pergunta_atual = 0
        
        # Frame principal
        self.frame_principal = ttk.Frame(janela)
        self.frame_principal.pack(expand=True)
        
        # Canvas para desenhar a imagem em blocos
        self.canvas = tk.Canvas(self.frame_principal, width=self.tamanho_imagem[0], 
                                height=self.tamanho_imagem[1], bg='black')
        self.canvas.pack(pady=20)
        
        # Calcular tamanho de cada bloco
        self.bloco_largura = self.tamanho_imagem[0] // self.grid_size
        self.bloco_altura = self.tamanho_imagem[1] // self.grid_size
        
        # Preparar blocos (nítidos e embaçados)
        self.preparar_blocos()
        
        # Label da pergunta/reflexão
        self.lbl_pergunta = ttk.Label(
            self.frame_principal,
            text=self.reflexoes[0]["pergunta"],
            font=("Arial", 20),
            foreground="black",
            wraplength=600
        )
        self.lbl_pergunta.pack(pady=10)
        
        # Frame para entrada de resposta
        self.frame_resposta = ttk.Frame(self.frame_principal)
        self.frame_resposta.pack(pady=10)
        
        # Label e campo de entrada
        self.lbl_instrucao = ttk.Label(
            self.frame_resposta,
            text="Digite sua resposta:",
            font=("Arial", 12)
        )
        self.lbl_instrucao.pack(side=tk.LEFT, padx=5)
        
        self.entry_resposta = ttk.Entry(
            self.frame_resposta,
            font=("Arial", 12),
            width=30
        )
        self.entry_resposta.pack(side=tk.LEFT, padx=5)
        self.entry_resposta.bind("<Return>", self.verificar_resposta)
        
        # Botão para verificar
        self.btn_verificar = ttk.Button(
            self.frame_resposta,
            text="Verificar",
            command=self.verificar_resposta
        )
        self.btn_verificar.pack(side=tk.LEFT, padx=5)
        
        # Label para feedback
        self.lbl_feedback = ttk.Label(
            self.frame_principal,
            text="",
            font=("Arial", 10),
            foreground="blue"
        )
        self.lbl_feedback.pack(pady=5)
        
        # Label para mostrar progresso
        self.lbl_progresso = ttk.Label(
            self.frame_principal,
            text=f"Pergunta {self.pergunta_atual + 1} de {len(self.reflexoes)} - Imagem embaçada",
            font=("Arial", 10),
            foreground="gray"
        )
        self.lbl_progresso.pack(pady=5)
        
        # Desenhar imagem inicial (toda preta)
        self.atualizar_canvas()
    
    def aplicar_borrao(self, imagem, raio=12):
        """Aplica efeito de borrão na imagem"""
        return imagem.filter(ImageFilter.GaussianBlur(radius=raio))
    
    def preparar_blocos(self):
        """Divide a imagem em blocos nítidos e cria versões embaçadas"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.bloco_largura
                y1 = i * self.bloco_altura
                x2 = x1 + self.bloco_largura
                y2 = y1 + self.bloco_altura
                
                # Recortar o bloco nítido da imagem
                bloco_nitido = self.imagem_redimensionada.crop((x1, y1, x2, y2))
                bloco_nitido_tk = ImageTk.PhotoImage(bloco_nitido)
                self.blocos_nitidos.append(bloco_nitido_tk)
                
                # Criar versão embaçada do bloco
                bloco_embacado = self.aplicar_borrao(bloco_nitido, raio=12)
                bloco_embacado_tk = ImageTk.PhotoImage(bloco_embacado)
                self.blocos_embacados.append(bloco_embacado_tk)
    
    def tornar_tudo_nitido(self):
        """Converte todos os blocos revelados para versão nítida"""
        self.imagem_nitida = True
        self.atualizar_canvas()
    
    def atualizar_canvas(self):
        """Desenha a imagem com os blocos revelados (embaçados ou nítidos)"""
        self.canvas.delete("all")
        
        for idx in range(len(self.blocos_nitidos)):
            i = idx // self.grid_size
            j = idx % self.grid_size
            x1 = j * self.bloco_largura
            y1 = i * self.bloco_altura
            
            if self.blocos_revelados[idx]:
                # Se a imagem já está nítida (após resposta5), mostrar versão NÍTIDA
                if self.imagem_nitida:
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.blocos_nitidos[idx])
                else:
                    # Senão, mostrar versão EMBACADA
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.blocos_embacados[idx])
            else:
                # Bloco oculto - mostra preto
                self.canvas.create_rectangle(x1, y1, x1 + self.bloco_largura, 
                                            y1 + self.bloco_altura, fill='black', outline='#333333')
    
    def revelar_blocos_da_pergunta(self):
        """Revela os blocos correspondentes à pergunta atual"""
        if self.pergunta_atual < len(self.revelacao_por_pergunta):
            blocos = self.revelacao_por_pergunta[self.pergunta_atual]
            for bloco_index in blocos:
                self.blocos_revelados[bloco_index] = True
            
            # Se for a última pergunta (índice 4), tornar TUDO NÍTIDO
            if self.pergunta_atual == 4:
                self.tornar_tudo_nitido()
            
            self.atualizar_canvas()
            
            # Calcular quantos blocos já foram revelados
            blocos_revelados_count = sum(self.blocos_revelados)
            
            # Atualizar texto do progresso
            if self.pergunta_atual == 4:
                self.lbl_progresso.config(
                    text=f"Pergunta {self.pergunta_atual + 1} de {len(self.reflexoes)} - ✨ IMAGEM COMPLETAMENTE NÍTIDA! ✨"
                )
            else:
                self.lbl_progresso.config(
                    text=f"Pergunta {self.pergunta_atual + 1} de {len(self.reflexoes)} - Imagem embaçada (blocos: {blocos_revelados_count}/9)"
                )
    
    def avancar_para_proxima_pergunta(self):
        """Avança para a próxima pergunta"""
        self.pergunta_atual += 1
        
        if self.pergunta_atual < len(self.reflexoes):
            # Atualizar texto da pergunta
            self.lbl_pergunta.config(text=self.reflexoes[self.pergunta_atual]["pergunta"])
            
            if self.pergunta_atual == 4:
                self.lbl_progresso.config(
                    text=f"Pergunta {self.pergunta_atual + 1} de {len(self.reflexoes)} - ⚠️ ÚLTIMA PERGUNTA! ⚠️"
                )
                self.lbl_feedback.config(text="Última pergunta! Ao acertar, a imagem ficará completamente NÍTIDA!", 
                                        foreground="purple")
            else:
                self.lbl_progresso.config(
                    text=f"Pergunta {self.pergunta_atual + 1} de {len(self.reflexoes)} - Imagem embaçada"
                )
                self.lbl_feedback.config(text="Próxima pergunta! Digite sua resposta.", foreground="blue")
            
            self.entry_resposta.delete(0, tk.END)
            self.entry_resposta.focus()
            self.btn_verificar.config(state="normal")
            self.entry_resposta.config(state="normal")
        else:
            # Todas as perguntas respondidas corretamente
            self.lbl_feedback.config(text="Parabéns! Você completou todas as reflexões e agora tem a imagem completamente nítida!", 
                                    foreground="green")
            self.btn_verificar.config(state="disabled")
            self.entry_resposta.config(state="disabled")
    
    def verificar_resposta(self, event=None):
        """Verifica se a resposta está correta"""
        resposta = self.entry_resposta.get().strip()
        resposta_correta = self.reflexoes[self.pergunta_atual]["resposta"]
        
        if resposta.lower() == resposta_correta.lower():
            # Acertou!
            self.revelar_blocos_da_pergunta()
            
            if self.pergunta_atual == 4:
                self.lbl_feedback.config(text="✓ PERFEITO! A imagem agora está completamente NÍTIDA! ✨", foreground="green")
            else:
                self.lbl_feedback.config(text="✓ Correto! Um novo bloco (embaçado) foi revelado!", foreground="green")
            
            self.entry_resposta.delete(0, tk.END)
            
            # Avançar para próxima pergunta após 1.5 segundos
            self.btn_verificar.config(state="disabled")
            self.entry_resposta.config(state="disabled")
            self.janela.after(1500, self.avancar_para_proxima_pergunta)
        else:
            # Errou
            self.lbl_feedback.config(text=f"✗ Resposta incorreta. Tente novamente!", foreground="red")
            self.entry_resposta.select_range(0, tk.END)
            self.entry_resposta.focus()

# Criar e executar aplicação
janela = tk.Tk()
app = Aplicacao(janela)
janela.mainloop()