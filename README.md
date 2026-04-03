# JogoFilosofia
Como funciona o jogo
Este é um jogo interativo que combina perguntas filosóficas com uma imagem que vai sendo revelada gradualmente. O jogador precisa responder corretamente a 5 reflexões para desbloquear completamente uma imagem.

Mecânica do jogo
Imagem em blocos: Uma imagem é dividida em uma grade 3x3 (9 blocos no total). Inicialmente, todos os blocos estão ocultos (tela preta). Cada resposta correta revela um ou mais blocos, mas eles aparecem embaçados (com efeito de desfoque). Apenas na última pergunta, ao acertar, a imagem se torna completamente nítida.

Sistema de perguntas: O jogo possui 5 reflexões pré-configuradas. Cada uma tem uma pergunta exibida para o jogador e uma resposta esperada que precisa ser digitada.

A cada acerto: o jogo revela os blocos correspondentes àquela pergunta, o texto de progresso é atualizado e o jogo avança automaticamente para a próxima pergunta.

Revelação dos blocos:

Pergunta 1: revela o bloco inferior esquerdo

Pergunta 2: revela o bloco inferior direito

Pergunta 3: revela o bloco inferior meio

Pergunta 4: revela os blocos do meio (esquerdo, centro e direito)

Pergunta 5: revela todos os blocos superiores e torna toda a imagem nítida

Interface do usuário
A aplicação oferece uma área para exibir a imagem em blocos, um campo de texto para digitar as respostas, botão de verificação (ou tecla Enter), feedback visual (verde para acerto, vermelho para erro), indicador de progresso mostrando quantos blocos já foram revelados e um timer automático de 1.5 segundos entre perguntas.

Tecnologias utilizadas
tkinter: interface gráfica

PIL (Pillow): manipulação de imagens (redimensionamento, recorte e efeito de desfoque GaussianBlur)

sys e os: gerenciamento de caminhos para compatibilidade com executável

Estrutura de arquivos necessária
O programa precisa de uma pasta "imagens" contendo o arquivo da imagem (por padrão, "rose-3061486_640.png") que será revelada ao longo do jogo.

Fluxo do jogo
O jogador vê a primeira pergunta filosófica e digita sua resposta. Se acertar, os blocos correspondentes são revelados (embaçados) e o jogo passa para a próxima pergunta. Se errar, pode tentar novamente sem penalidade. Ao acertar a quinta pergunta, a imagem fica completamente nítida e o jogo termina.

Características especiais
Os blocos revelados ficam embaçados até o final, criando expectativa. Diferentes perguntas revelam diferentes quantidades de blocos. Apenas ao acertar a reflexão final a imagem se torna cristalina. Feedback colorido orienta o jogador durante todo o processo.

Personalização
Você pode modificar as perguntas e respostas na lista "reflexoes", escolher quais blocos são revelados por pergunta na lista "revelacao_por_pergunta", substituir a imagem usada na pasta "imagens", alterar o tamanho da grade ou o raio do efeito de desfoque.

