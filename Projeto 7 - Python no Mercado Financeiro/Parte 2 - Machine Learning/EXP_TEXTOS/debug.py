class Aluno:
    def __init__(self, nome, nota1, nota2):
        self.nome = nome
        self.nota1 = nota1
        self.nota2 = nota2

    def media(self):
        return (self.nota1 + self.nota2) / 2
    
    def mostra_dados(self):
        print(f'Nome: {self.nome} \n')
        print(f'Nota 1: {self.nota1} \n')
        print(f'Nota 2: {self.nota2} \n')

    def resultado(self):
        if (self.nota1 + self.nota2) / 2 >= 6:
            print('Aprovado')
        else:
            print('Reprovado')

aluno1 = Aluno('Heitor', 8, 9)
aluno2 = Aluno('Z', 10, 7)

aluno1.mostra_dados()
print(aluno1.media())     
aluno1.resultado() 

print('\n')

aluno2.mostra_dados()
print(aluno2.media())     
aluno2.resultado()


   