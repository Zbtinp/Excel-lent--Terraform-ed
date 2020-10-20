import math

import numpy
import pandas as pd

sheet1 = pd.read_excel("aws_info.xlsx", 0) # AWS instances
sheet2 = pd.read_excel("aws_info.xlsx", 1) # AWS security groups
sheet3 = pd.read_excel("aws_info.xlsx", 2) # Ingress / Egress
sheet4 = pd.read_excel("aws_info.xlsx", 3) # SSH Key
sheet5 = pd.read_excel("aws_info.xlsx", 4) # Provider

config = '';



def build_provider(colnames, row):
    setup = 'provider "aws" {\n '
    for col in range(0, colnames.size):
        setup += colnames[col].replace(' ', '_').lower() + ' = "' + str(sheet5.iloc[row][col]) + '" \n '
    setup += '} \n \n'
    return setup

for row in range(0, sheet5.shape[0]):
    config += build_provider(sheet5.columns, row)

def build_ssh_keys(colnames, row):
    setup = 'resource "tls_private_key" "key' + str(row+1) + '" { \n '
    tls_key = 'tls_private_key.key' + str(row+1)
    for col in range(1, colnames.size):
        setup += colnames[col].replace(' ', '_').lower() + ' = ' + str(sheet4.iloc[row][col]) + '\n '
    setup += '} \n \n'
    setup += 'resource "aws_key_pair" "genkey' + str(row + 1) + '" { \n '
    setup += colnames[0].replace(' ', '_').lower() + ' = ' + str(sheet4.iloc[row][0]) + '\n '
    setup += 'public_key = "${' + tls_key + '.public_key_openssh}" \n '
    setup += '} \n \n'
    return setup

for row in range(0, sheet4.shape[0]):
    config += build_ssh_keys(sheet4.columns, row)

def build_security_groups(colnames_sec, row, colnames_ie):
    ing = []
    eg = []
    setup = 'resource "aws_security_group" "' + str(sheet2.iloc[row][0]) + '" { \n '

    # for name and description
    for col in [0, 7]:
        setup += colnames_sec[col].replace(' ', '_').lower() + ' = "' + str(sheet2.iloc[row][col]) + '" \n '
    setup += '\n '
    # for ingress and egress to be added
    for col in range(1, 7):
        if('Ingress' in colnames_sec[col] and str(sheet2.iloc[row][col]) != 'nan'):
            ing.append(str(sheet2.iloc[row][col]))
        elif('Egress' in colnames_sec[col] and str(sheet2.iloc[row][col]) != 'nan'):
            eg.append(str(sheet2.iloc[row][col]))

    while(len(ing) != 0):
        temp = ing.pop()
        for row in range(0, sheet3.shape[0]):
            if(sheet3.iloc[row][0] == 'ingress' and sheet3.iloc[row][1] == temp):
                setup += 'ingress { \n  '
                for col in range(0, sheet3.shape[1]):
                    setup += colnames_ie[col].replace(' ', '_').lower() + ' = "' + str(sheet3.iloc[row][col]) + '" \n  '
                setup += '} \n \n'

    while (len(eg) != 0):
        temp = eg.pop()
        for row in range(0, sheet3.shape[0]):
            if (sheet3.iloc[row][0] == 'egress' and sheet3.iloc[row][1] == temp):
                setup += 'egress { \n  '
                for col in range(0, sheet3.shape[1]):
                    setup += colnames_ie[col].replace(' ', '_').lower() + ' = "' + str(sheet3.iloc[row][col]) + '" \n  '
                setup += '} \n \n'

    setup += '} \n \n'
    return setup

for row in range(0, sheet2.shape[0]):
    config += build_security_groups(sheet2.columns, row, sheet3.columns)


outfile = open("test.tf", "w+")
outfile.write(config)
outfile.close
