"""                   Comentários de várias linhas.
  CEUB  -  FATECS  -  BCC  -  ADS  -  Programação  -  Prof. Barbosa
ctlr<d>, duplica linha. ctrl<y>, apaga linha. ctrl</>, comenta linha.

- Veja a teoria no arquivo "Teoria POO MySQL.docx"

- Coloque todos os programas num único arquivo .py com várias funções (defs)
e a função main para controlar o funcionamento do sistema, chamar as funções.

Obs.: crie um projeto novo e um arquivo.py dentro do projeto.

- Implemente:
1. Crie a função create connection, ela faz a conexão com o servidor e
   retorna a conexão criada para o main.
2. Crie a função main no mesmo arquivo das funções, chame a função create
   connection e depois crie o cursor.
3. Crie a função create database e informe qual o database que queremos usar
   nos próximos comandos SQL, ou seja, ative o database criado.
4. Na função main, chame a função create database e ative o database para uso.
5. Na base de dados db_cadastro, modele os dados de um empregado com estas
   características:
    O nome do empregado;
    A data de nascimento;
    O gênero; e
    O nome do cargo.
Como modelar?
- Relacionamento das tabelas:
    tb_empregado | ()     ------------    ()  | tb_cargo
    tb_empregado | (n)    ------------    (1) | tb_cargo
    idt (pk)                                    idt (pk)
    nome                                        nome
    dta_nascimento
    genero
    cod_cargo (fk)
Obs.: use pelo menos uma coluna obrigatória, opcional, sem repetição e enumarada
      com domínio de valores
- tb_cargo                      # td - tabela de domínio
    idt             (pk automático)
    nome            (obrigatória e sem repetição)
- tb_empregado                  # tb - tabela básica
    idt             (pk automático)
    nome            (obrigatória)
    dta_nascimento  (opcional)
    genero          (obrigatória, enumerada com domínio de valores: M ou F)
    cod_cargo       (fk)
6. Na função main, chama a função create table
7. Devemos inserir os dados primeiro na tabela tb_cargo ou na tabela tb_empregado?
8. Crie a função insert cargo com inputs. No main, chame a função
9. Crie a função insert empregado com inputs. No mein, chame a função
10. Crie a função select all de tb_cargo. No main, chame a função
11. Crie a função select all empregado. No main, chame a função
12. Crie a função select all empregado usando notação de vetor. No main, teste
13. Melhore a função select all empregado para mostrar o nome do cargo ao
   invés de mostrar o código do cargo. No main, teste

"""

import mysql.connector
def create_connection():
    conexao = mysql.connector.connect(user='root',  # user do servidor
                            password='ceub123456',            # passwd='ceub123456'
                            host='127.0.0.1')       # host='localhost'
                            # database='')
    print('Conexão db:', conexao)  # Teste
    return conexao
def create_database():
    sql_create = "CREATE DATABASE if not exists db_cadastro"  # O nome do database
    cursor.execute(sql_create)        # Executa o comando sql
    sql_use = "use db_cadastro"
    cursor.execute(sql_use)           # Executa o comando SQL
def create_table():
    sql_cargo = """ CREATE TABLE IF NOT EXISTS tb_cargo ( 
    idt int NOT NULL AUTO_INCREMENT,  # Cria automaticamente a chava primária
    nome varchar(45) NOT NULL UNIQUE, # Valores sem repetição
    PRIMARY KEY (idt)                 # Define a chave primária
    )   """                           # Fecha parênteses bbrigatório
    cursor.execute(sql_cargo)         # Primeiro, crie a tabela tb_cargo
    # Use aspas duplas ("""), senão dá erro por causa do enum('M', 'F'), aspas simples
    sql_empregado = """ CREATE TABLE IF NOT EXISTS tb_empregado (
    idt int NOT NULL AUTO_INCREMENT,  # Cria automaticamente a chava primária
    nome varchar(45) NOT NULL,        # NOT NULL para valor obrigatório
    dta_nascimento date NULL,         # NULL para valor opcional
    genero enum('M', 'F') NOT NULL,   # Aceita 'M', 'm, 'F' ou 'f' 
    cod_cargo int NOT NULL,           # NOT NULL para valor obrigatório
    PRIMARY KEY (idt),                # Define a chave primária
    FOREIGN KEY(cod_cargo) REFERENCES tb_cargo(idt)  # Chave estrangeira
    )   """                           # Fecha parênteses bbrigatório
    cursor.execute(sql_empregado)     # Depois, crie a tabela tb_empregado
def insert_cargo():                   # Solução 1
    a_nome = input('Nome do cargo: ')  # Insere primeiro na tabela domínio
    sql = f"""  insert into tb_cargo (nome)
                values('{a_nome}')              """
    cursor.execute(sql)
    conexao.commit()                  # Confirma a alteração no database, obrigatório
    print('Registros inseridos:', cursor.rowcount)
def insert_empregado():               # Solução 1
    # Inserir primeiro os dados na tabela domínio, tb_cargo
    a_nome = input('Nome empregado: ')
    a_genero = input("Gênero [M] ou [F]: ")
    from datetime import date
    a_dta_nascimento = date.today()
    a_cod_cargo = int(input('FK - Código Cargo: '))
    sql = f"""insert into tb_empregado 
    (nome, dta_nascimento, genero, cod_cargo)
    values('{a_nome}', '{a_dta_nascimento}', '{a_genero}', {a_cod_cargo})  """
    cursor.execute(sql)
    conexao.commit()        # Confirma a alteração no database, obrigatório
def select_all_emp():
    sql = ''' select * from tb_empregado '''
    cursor.execute(sql)
    registros = cursor.fetchall()   # registros é uma lista de tuplas
    print('- List of tuplas:')      # Solução 1:
    print(registros)                # Mostra os registros na horizontal
    print('- Tuplas:')              # Solução 2:
    for record in registros:        # Mostra os registros na vertical
        print(record)
def select_all_join():
    # Alias no nome de tabela no from e prefixo no nome de coluna no select
    sql = ''' select e.nome, e.dta_nascimento, e.genero, c.nome
              from tb_empregado as e inner join tb_cargo as c
              where e.cod_cargo = c.idt                         '''
    # sql = ''' select e.nome, e.dta_nascimento, e.genero, c.nome
    #           from tb_empregado as e inner join tb_cargo as c
    #                on e.cod_cargo = c.idt                     '''
    cursor.execute(sql)
    registros = cursor.fetchall()   # registros é uma lista de tuplas
    print('\n- List of tuplas:')                        # Solução 1:
    print(registros)                # Mostra os registros na horizontal
    print('\n- Tuplas:')                                # Solução 2:
    for record in registros:        # Mostra os registros na vertical
        print(record)


if __name__ == '__main__':
    conexao = create_connection()  # Chama a função
    cursor = conexao.cursor()      # Cria cursor para executar os comandos SQL
    create_database()              # Chama a função
    create_table()                 # Chama a função
    insert_cargo()                 # Chama a função
    insert_empregado()             # Chama a função
    select_all_emp()               # Chama a função
    select_all_join()








// Criando objetos para cada personagem

let dva = {
    titulo: 'D.va',
    descricao: 'D.Va, cujo nome real é Hana Song, é uma personagem vibrante e cheia de energia do universo de Overwatch. Conhecida mundialmente como a melhor jogadora de StarCraft II, ela trocou a vida de gamer profissional para defender sua cidade natal, a Coreia do Sul.',
    link: 'https://overwatch.fandom.com/wiki/D.Va',
    tags: 'MEKA CoreiaDoSul Gamer Tank Mech Overwatch2'
}

let doomfist = {
    titulo: 'Doomfist',
    descricao: 'Doomfist é um dos personagens mais imponentes e enigmáticos de Overwatch. Um líder carismático e implacável, ele comanda a Talon, uma organização terrorista que busca moldar o mundo à sua própria imagem.',
    link: 'https://overwatch.fandom.com/wiki/Doomfist',
    tags: 'Talon Líder Poder Luta Overwatch2'
}

let junkerqueen = {
    titulo: 'Junker Queen',
    descricao: 'Junker Queen, ou Odessa "Dez" Stone, é uma das personagens mais imponentes e carismáticas de Overwatch 2. Uma líder nata, ela comanda os Junkers, um grupo de sobreviventes que habitam os escombros de uma cidade pós-apocalíptica.',
    link: 'https://overwatch.fandom.com/wiki/Junker_Queen',
    tags: 'Junkers Líder Austrália PósApocalíptico Overwatch2'
}

let mauga = {
    titulo: 'Mauga',
    descricao: 'Com um passado repleto de batalhas e uma força sobre-humana, Mauga é um verdadeiro tanque. Seu corpo, modificado por avançados procedimentos cirúrgicos, lhe confere uma resistência e força incríveis. Suas cicatrizes contam histórias de uma vida dedicada à luta e à sobrevivência.',
    link: 'https://overwatch.fandom.com/wiki/Mauga',
    tags: 'Tank ForçaBruta Sobrevivente Militar Overwatch2'
}

let orisa = {
    titulo: 'Orisa',
    descricao: 'Orisa é uma heroína tanque de Overwatch 2, criada pela jovem e brilhante Efi Oladele para proteger a cidade de Numbani. Essa robô imponente é conhecida por sua força, durabilidade e habilidades defensivas excepcionais.',
    link: 'https://overwatch.fandom.com/wiki/Orisa',
    tags: 'Robô Defesa Numbani InteligênciaArtificial Overwatch2'
}

let ramattra = {
    titulo: 'Ramattra',
    descricao: 'Ramattra é um dos heróis tanques mais recentes de Overwatch 2, um ômnico com uma história complexa e um desejo ardente de moldar o futuro da sua espécie. Ele é conhecido por sua capacidade de se transformar entre duas formas, cada uma com suas próprias habilidades e vantagens.',
    link: 'https://overwatch.fandom.com/wiki/Ramattra',
    tags: 'Ômnico Transformação Filosofia Liderança Overwatch2'
}

let reinhardt = {
    titulo: 'Reinhardt',
    descricao: 'Reinhardt Wilhelm é um dos personagens mais icônicos de Overwatch 2, um tanque poderoso e imponente que inspira seus aliados com sua coragem e lealdade. Com seu martelo colossal, o Martelo de Justiça, Reinhardt é uma força a ser considerada em qualquer campo de batalha.',
    link: 'https://overwatch.fandom.com/wiki/Reinhardt',
    tags: 'Cruzado Martelo Líder Alemanha Overwatch2'
}

let roadhog = {
    titulo: 'Roadhog',
    descricao: 'Roadhog, ou mais conhecido como Mako Rutledge, é um dos tanques mais intimidantes de Overwatch 2. Esse ex-policial de Numbani, transformado em um mercenário brutal, é conhecido por sua força bruta, resistência e apetite insaciável. Seu visual imponente, com cicatrizes e tatuagens, reflete sua vida violenta e cheia de perigos.',
    link: 'https://overwatch.fandom.com/wiki/Roadhog',
    tags: 'Junkers Austrália Mercenário ForçaBruta Overwatch2'
}

let sigma = {
    titulo: 'Sigma',
    descricao: 'Sigma, cujo nome real é desconhecido, é um cientista brilhante que experimentou com a manipulação da gravidade. Seus experimentos, no entanto, deram errado, causando uma catástrofe que alterou sua forma física e lhe concedeu poderes gravitacionais extraordinários.',
    link: 'https://overwatch.fandom.com/wiki/Sigma',
    tags: 'Cientista Gravidade Poder Experimentos Overwatch2'
}

let winston = {
    titulo: 'Winston', 
    descricao: 'Winston, o cientista gorila, é um dos heróis mais inteligentes e poderosos de Overwatch. Com sua força bruta e tecnologia avançada, ele luta para proteger a humanidade e criar um futuro melhor para todos.',
    link: 'https://overwatch.fandom.com/wiki/wiki/Winston',
    tags: 'Cientista Gorila Inteligência Overwatch Winton'
};


let wreckingBall = {
    titulo: 'Wrecking Ball',
    descricao: 'Hammond, mais conhecido como Wrecking Ball, é um personagem peculiar e divertido de Overwatch 2. Esse pequeno hamster robótico, originalmente um experimento da Colônia Lunar Horizon, encontrou seu lugar entre os Junkers de Junkertown, transformando sua cápsula de escape em um poderoso mecha de batalha.',
    link: 'https://overwatch.fandom.com/wiki/Wrecking_Ball',
    tags: 'Hamster Robô Junkertown Austrália Overwatch2'
}

let zarya = {
    titulo: 'Zarya',
    descricao: 'Zarya, ou Aleksandra Zaryanova, é uma das personagens mais poderosas e carismáticas de Overwatch 2. Uma ex-campeã de levantamento de peso, Zarya se tornou uma força a ser reconhecida, utilizando sua força sobre-humana para proteger sua comunidade.',
    link: 'https://overwatch.fandom.com/wiki/Zarya',
    tags: 'Força Rússia Atleta Proteção Overwatch2'
}

let ashe = {
    titulo: 'Ashe',
    descricao: 'Ashe, a líder ambiciosa e calculista da gangue Deadlock, é uma figura imponente e respeitada no submundo do crime. Nascida em uma família rica, Ashe logo se rebelou contra a vida de privilégios e construiu seu próprio império.',
    link: 'https://overwatch.fandom.com/wiki/Ashe',
    tags: 'DeadlockGang Pistoleira Liderança Vingança Overwatch2'
}

let bastion = {
    titulo: 'Bastion',
    descricao: 'Bastion é um personagem peculiar e fascinante de Overwatch 2. Originalmente criado como uma máquina de guerra, Bastion passou por uma transformação radical, desenvolvendo uma curiosidade pela natureza e pela vida.',
    link: 'https://overwatch.fandom.com/wiki/Bastion',
    tags: 'Robô Transformação Natureza Paz Overwatch2'
}

let cassidy = {
    titulo: 'Cassidy',
    descricao: 'Cassidy, anteriormente conhecido como Cole Cassidy, é um personagem icônico de Overwatch 2, um pistoleiro solitário com um passado turbulento. Sua habilidade com as armas e seu senso de justiça o tornaram uma figura lendária no mundo dos jogos.',
    link: 'https://overwatch.fandom.com/wiki/Cassidy',
    tags: 'Pistoleiro Solitário Vingança Overwatch2 Jesse McCree McCree'
}

let echo = {
    titulo: 'Echo',
    descricao: 'Echo é uma heroína omnic extremamente avançada em Overwatch 2, com a habilidade única de duplicar outros heróis. Sua história é um tanto misteriosa, mas sabemos que ela foi criada com um propósito: coletar dados e informações.',
    link: 'https://overwatch.fandom.com/wiki/Echo',
    tags: 'Ômnico Duplicação InteligênciaArtificial Overwatch2'
}

let genji = {
    titulo: 'Genji',
    descricao: 'Genji Shimada é um ciborgue ninja, membro da poderosa família Shimada. Após uma tentativa de assassinato que o deixou gravemente ferido, Genji foi reconstruído como um ninja cibernético,',
    link: 'https://overwatch.fandom.com/wiki/Genji',
    tags: 'Ninja Shimada Cibernético Honra Overwatch2 Nerf'
}

let hanzo = {
    titulo: 'Hanzo',
    descricao: 'Hanzo era originalmente um membro da poderosa clã Shimada, uma organização criminosa japonesa. Ele foi criado para seguir os passos de seu irmão mais velho, Genji, mas seu caminho se desviou quando ele escolheu um caminho diferente. A rivalidade entre os irmãos culminou em um confronto trágico, no qual Hanzo acreditou ter matado Genji.',
    link: 'https://overwatch.fandom.com/wiki/Hanzo',
    tags: 'Shimada Arqueiro Natureza Família Overwatch2'
}

let junkrat = {
    titulo: 'Junkrat',
    descricao: 'Junkrat é um personagem excêntrico e perigoso de Overwatch 2, conhecido por sua obsessão por explosivos. Ele nasceu e cresceu em Junkertown, uma cidade pós-apocalíptica na Austrália,',
    link: 'https://overwatch.fandom.com/wiki/Junkrat',
    tags: 'Explosivos Austrália Junkertown Louco Overwatch2'
}

let mei = {
    titulo: 'Mei',
    descricao: 'Mei-Ling Zhou, mais conhecida como Mei, é uma cientista chinesa que se tornou uma heroína em Overwatch 2. Sua jornada é marcada por uma profunda preocupação com o meio ambiente e uma missão de proteger o planeta.',
    link: 'https://overwatch.fandom.com/wiki/Mei',
    tags: 'Cientista Gelo MeioAmbiente China Overwatch2'
}

let pharah = {
    titulo: 'Pharah',
    descricao: 'Fareeha Amari, mais conhecida como Pharah, é uma heroína de Overwatch 2 que domina os céus com sua agilidade e poder de fogo. Inspirada por sua mãe, a lendária sniper Ana Amari, Pharah se tornou uma piloto de elite e uma força a ser considerada no campo de batalha.',
    link: 'https://overwatch.fandom.com/wiki/Pharah',
    tags: 'Piloto MãeSonharica Egito Missões Overwatch2'
}

let reaper = {
    titulo: 'Reaper',
    descricao: 'Antes de se tornar o Ceifador, Reaper era conhecido como Gabriel Reyes, um dos fundadores da Overwatch. No entanto, após um trágico incidente, Reyes se tornou amargo e desiludido, abandonando a organização e se tornando um mercenário.',
    link: 'https://overwatch.fandom.com/wiki/Reaper',
    tags: 'Talon Assassino Sombras Vingança Overwatch2'
}

let soujourn = {
    titulo: 'Soujourn',
    descricao: 'Soujourn é uma líder nata, com uma mente estratégica e um senso de justiça inabalável. Ela foi uma das primeiras a experimentar a tecnologia de armadura de energia, que lhe concede habilidades únicas e poderosas no campo de batalha.',
    link: 'https://overwatch.fandom.com/wiki/Sojourn',
    tags: 'Líder Tecnologia Justica Overwatch2'
}

let soldado76 = {
    titulo: 'Soldado: 76',
    descricao: 'Soldado: 76, cujo nome real é Jack Morrison, é um dos personagens mais emblemáticos de Overwatch 2. Ele é um veterano da Overwatch original, um dos seus fundadores e um dos últimos soldados aprimorados geneticamente. Após a queda da Overwatch, Soldado: 76 se tornou um vigilante, buscando a verdade por trás da destruição da organização que um dia liderou.',
    link: 'https://overwatch.fandom.com/wiki/Soldier:_76',
    tags: 'Líder Veterano Overwatch Justica Overwatch2'
}

let sombra = {
    titulo: 'Sombra',
    descricao: 'Nascida no México, Sombra perdeu seus pais durante a Crise Ômnica e cresceu nas ruas, aprendendo a sobreviver com sua inteligência e habilidades de hacker. Suas habilidades a levaram a se juntar à Talon, uma organização criminosa que busca minar a ordem mundial.',
    link: 'https://overwatch.fandom.com/wiki/Sombra',
    tags: 'Hacker Talon México Inteligência Overwatch2'
}

let symmetra = {
    titulo: 'Symmetra',
    descricao: 'Symmetra foi criada para proteger a Vishkar Corporation, uma empresa tecnológica global. Suas habilidades foram desenvolvidas para proteger instalações e controlar fluxos de pessoas. Após a queda da Vishkar, Symmetra se tornou uma heroína independente, usando seus poderes para ajudar os outros.',
    link: 'https://overwatch.fandom.com/wiki/Symmetra',
    tags: ' Arquiteta Vishkar Tecnologia Índia Overwatch2'
}

let tracer = {
    titulo: 'Tracer', 
    descricao: 'Tracer, cujo nome verdadeiro é Lena Oxton, é uma personagem vibrante e cheia de energia que conquistou o coração dos jogadores de Overwatch. Com sua habilidade única de manipular o tempo, ela se tornou um ícone do jogo, representando a esperança e a positividade em um mundo incerto.',
    link: 'https://overwatch.fandom.com/wiki/Tracer',
    tags: 'Tempo Agente Esperança Britânia Overwatch2'
};


let torbjorn = {
    titulo: 'Torbjörn',
    descricao: 'Torbjörn Lindholm é um engenheiro sueco brilhante e um dos membros fundadores da Overwatch. Conhecido por sua paixão por construir e por sua personalidade um tanto explosiva, Torbjörn desempenhou um papel crucial na criação de muitas das tecnologias avançadas que a Overwatch utilizava.',
    link: 'https://overwatch.fandom.com/wiki/Torbjorn',
    tags: 'Engenheiro Suécia Construção Overwatch2'
}

let venture = {
    titulo: 'Venture',
    descricao: 'Venture, também conhecido como Sloan Cameron, tinha uma habilidade especial para encontrar coisas perdidas desde a infância. Eles viajavam muito, e cada novo lar representava uma nova expedição. Essa habilidade os levou à Sociedade Wayfinder, onde começaram um aprendizado aos 16 anos. Com coragem inabalável, enfrentavam ruínas antigas e omniums desativados, retornando sempre com descobertas valiosas. Além disso, Cameron ajudava na segurança dos artefatos da Sociedade, enfrentando saqueadores e ladrões com suas ferramentas de escavação e inteligência rápida.',
    link: 'https://overwatch.fandom.com/wiki/Venture',
    tags: 'Explorador SociedadeWayfinder Descoberta Aventura Overwatch2'
}

let widowmaker = {
    titulo: 'Widowmaker',
    descricao: 'Widowmaker, cujo nome verdadeiro é Amélie Lacroix, é uma das personagens mais enigmáticas e perigosas de Overwatch. Transformada em uma máquina de matar pela organização terrorista Talon, ela é a personificação da letalidade fria e calculada.',
    link: 'https://overwatch.fandom.com/wiki/Widowmaker',
    tags: 'Assassina Talon França Letalidade Overwatch2'
}

let ana = {
    titulo: 'Ana',
    descricao: 'Ana vem de uma longa linhagem de militares e esteve presente desde o início da Overwatch, organização criada para promover a paz após a Crise Ômnica. Sua experiência e habilidade com armas de longo alcance foram cruciais para o sucesso inicial da equipe.',
    link: 'https://overwatch.fandom.com/wiki/Ana',
    tags: 'Sniper Curadora Mãe Egito Overwatch'
}

let baptiste = {
    titulo: 'Baptiste',
    descricao: 'Originário de uma região devastada pela guerra, Baptiste era um médico de combate talentoso. Atraído pela promessa de riqueza fácil, ele se juntou à Talon, uma organização terrorista, oferecendo seus serviços como médico. No entanto, a brutalidade das missões da Talon, que incluíam assassinatos e operações com baixas civis, o fizeram questionar suas escolhas.',
    link: 'https://overwatch.fandom.com/wiki/Baptiste',
    tags: 'Médico Curador Tecnologia Haiti Overwatch2'
}

let brigitte = {
    titulo: 'Brigitte',
    descricao: 'Desde jovem, Brigitte mostrou um talento natural para a engenharia, seguindo os passos de seu pai. Ela passou horas em sua oficina, construindo e aperfeiçoando suas criações. No entanto, sua verdadeira paixão era a aventura e a proteção. Inspirada pelas histórias de seu padrinho, Reinhardt, ela decidiu se tornar sua escudeira.',
    link: 'https://overwatch.fandom.com/wiki/Brigitte',
    tags: 'Suporte Engenheira Escudera Suécia Overwatch2'
}

let illari = {
    titulo: 'Illari',
    descricao: 'Illari cresceu treinando para se tornar uma Guerreira Inti, uma ordem de protetores sagrados que canalizam o poder do sol. Sua vida era dedicada a dominar suas habilidades solares e a servir à sua comunidade. No entanto, um trágico acidente levou à morte de todos os outros Guerreiros Inti,',
    link: 'https://overwatch.fandom.com/wiki/Illari',
    tags: 'Sol Curadora Guerreira Peru Overwatch2'
}

let juno = {
    titulo: 'Juno',
    descricao: 'Juno cresceu em uma colônia marciana, cercada por tecnologia de ponta e a imensidão do espaço. Desde pequena, ela demonstrou uma curiosidade insaciável e uma paixão por ajudar os outros. Com o tempo, ela se tornou uma engenheira brilhante, desenvolvendo novas tecnologias para melhorar a vida em Marte.',
    link: 'https://overwatch.fandom.com/wiki/Juno',
    tags: 'Engenheira Marte Exploração Tecnologia Overwatch2'
}

let kiriko = {
    titulo: 'Kiriko',
    descricao: 'Kiriko cresceu em um ambiente rico em tradições e espiritualidade. Desde tenra idade, ela demonstrou um talento natural para a cura e a proteção, habilidades que foram aprimoradas com o treinamento rigoroso no santuário de Kanezaka. Sua conexão profunda com o espiritual a permite manipular a energia ki, concedendo-lhe poderes sobrenaturais.',
    link: 'https://overwatch.fandom.com/wiki/Kiriko',
    tags: 'Ninja Curadora Espiritualidade Japão Overwatch2'
}

let lifeweaver = {
    titulo: 'Lifeweaver',
    descricao: 'A história de Lifeweaver é marcada por um profundo desejo de ajudar os outros e um conflito constante com as forças que buscam explorar suas criações para fins egoístas. Ele é um fugitivo, sempre um passo à frente da Vishkar, enquanto trabalha incansavelmente para aperfeiçoar sua tecnologia e espalhar a cura pelo mundo.',
    link: 'https://overwatch.fandom.com/wiki/Lifeweaver',
    tags: 'Curador Tecnologia Natureza Fuga Overwatch2'
}

let lucio = {
    titulo: 'Lúcio',
    descricao: 'Lúcio cresceu em uma cidade dividida por conflitos sociais e econômicos. Inspirado pela música, ele decidiu usar seu talento para unir as pessoas e criar um futuro melhor. Com suas batidas eletrizantes, Lúcio espalhou esperança e uniu as comunidades, transformando-se em um símbolo de resistência contra a opressão.',
    link: 'https://overwatch.fandom.com/wiki/Lucio',
    tags: 'DJ Música Brasil União Overwatch2 GOAT FROGGER'
}

let mercy = {
    titulo: 'Mercy',
    descricao: 'Mercy se destacou como uma prodigiosa cientista, pioneira em nanotecnologia. Sua paixão por salvar vidas a levou a se tornar a médica de combate mais renomada da Overwatch. Com sua tecnologia de ponta e habilidades de cura, ela se tornou um símbolo de esperança e resiliência para muitos.',
    link: 'https://overwatch.fandom.com/wiki/Mercy',
    tags: 'Curadora Cientista Suíça Esperança Overwatch2'
};

let moira = {
    titulo: 'Moira',
    descricao: 'Moira é uma mente científica brilhante, obcecada pela evolução humana. Seus experimentos genéticos a levaram a descobrir novas formas de manipular a vida, mas também a criar criaturas horríveis e a colocar em risco a humanidade. Sua ambição ilimitada a torna uma figura enigmática e fascinante.',
    link: 'https://overwatch.fandom.com/wiki/Moira',
    tags: 'Cientista Genética Manipulação Poder Overwatch2'
}

let zenyatta = {
    titulo: 'Zenyatta',
    descricao: 'Zenyatta, um dos primeiros ômnicos a alcançar a consciência, busca um equilíbrio entre a mente e o corpo. Ele acredita que a violência não é a resposta para os problemas do mundo e que a harmonia pode ser alcançada através da meditação e da compreensão mútua.',
    link: 'https://overwatch.fandom.com/wiki/Zenyatta',
    tags: 'Ômnico Meditação Harmonia Sabedoria Overwatch2'
}

// Adicionando os objetos a uma lista
let dados = [tracer, winston, mercy, ana, dva, doomfist, junkerqueen, mauga, orisa, ramattra, reinhardt, roadhog, sigma, wreckingBall, zarya, ashe, bastion, cassidy, echo, genji, hanzo, junkrat, mei, pharah, reaper, soujourn, soldado76, sombra, symmetra, torbjorn, venture, widowmaker, baptiste, brigitte, illari, juno, kiriko, lifeweaver, lucio, moira, zenyatta];