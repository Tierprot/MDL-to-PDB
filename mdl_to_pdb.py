__author__ = 'Bones'

"""This script can be shared on the basis of "THE BEER-WARE LICENSE" (Revision 42)"""

def process_line(input_line):
    string = input_line.strip()
    string = string.split()
    return string


def spaces(input_value, filename,max_spaces):
    blank = max_spaces - len(str(input_value))
    while blank != 0:
        filename.write(" ")
        blank -= 1


inputname =  input("Welcome to converter from MDL molfile [V2000] (.mol) into PDB (.pdb)\nType filename of file to be converted:\n")
inputname += ".mol"
outputname = inputname[:-3] + "pdb"

with open(inputname, "r") as inputfile:
    with open(outputname, "w") as outputfile:
        token = 0
        connection_numbers = 0
        coordinates = 0
        pair_list = []
        MAX_COOR = 0
        MAX_CON = 0
        for line in inputfile:

            token += 1

            # строка с информацией о количестве атомов и связей
            if token == 4:
                header = process_line(line)

                coordinates = int(header[0])
                MAX_COOR = coordinates

                connection_numbers = int(header[1])
                MAX_CON = connection_numbers

            # выпечатываем форматированный под pdb вид координат
            elif token > 4 and coordinates > 0:
                c_line = process_line(line)
                outputfile.write("HETATM")

                #выравнивение пробелами
                spaces((-1 * (coordinates - MAX_COOR) + 1), outputfile,5)

                outputfile.write("{atom_number}  {atom_type}   LIG     1     ".
                                 format(atom_number=(-1 * (coordinates - MAX_COOR)) + 1, atom_type=c_line[3]))

                #координаты с выравнивением пробелами
                for i in range(3):
                    outputfile.write("{:>7.3f} ".format(float(c_line[i])))

                outputfile.write(" 1.00  1.00          {atom_type}\n".format(atom_type=c_line[3]))

                coordinates -= 1

            #набираем массив пар для CONNECT
            elif token > 4 and coordinates == 0 and connection_numbers > 0:
                c_line = process_line(line)
                c_line = c_line[:2]
                pair_list.append(c_line)

                connection_numbers -= 1

        # cделаем пары чисел числами
        pairs = [[int(y) for y in x] for x in pair_list]

        #для каждого номера от 1 до MAX_COOR ищем контакты
        for number in range(1, MAX_COOR + 1):

            outputfile.write("CONECT")

            #генерируем правильное число пробелов
            spaces(number, outputfile,5)

            outputfile.write("{atom}".format(atom=number))

            connections_set = set()

            for i in range(MAX_CON):
                #выписываем все атомы в которых участвует атом под номером number
                if number in pairs[i]:
                    connections_set.update(pairs[i])
            connections_set = list(connections_set)

            #удаляем атом относительно которого и формировали контакты
            connections_set.remove(number)
            #сортируем
            connections_set.sort()

            #записываем контакты
            for i in range(len(connections_set)):
                spaces(connections_set[i], outputfile,5)
                outputfile.write("{atom}".format(atom=connections_set[i]))
            outputfile.write("\n")

        outputfile.write("MASTER      0    0    0    0    0    0    0    {num_coord}    0    {num_connect}    0\nEND".
                         format(num_coord=MAX_COOR, num_connect=MAX_CON))

print("Seems everything worked fine - enjoy!\nFound bug? Mail me: bones@phys.protres.ru")

