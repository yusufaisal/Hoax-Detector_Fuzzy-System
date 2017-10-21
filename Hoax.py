from __future__ import division

#Stabil
nStabilAwal = 0
nStabilAkhir = 20
#Cukup Stabil
nCukupStabilAwal = 50
nCukupStabilAkhir = 60
#Tidak Stabil
nTidakStabilAwal = 80
nTidakStabilAkhir = 100

#Normal
nNormalAwal = 0
nNormalAkhir = 45
#Cukup Normal
nCukupNormalAwal = 60
nCukupNormalAkhir = 70
#Tidak Normal
nTidakNormalAwal = 80
nTidakNormalAkhir = 100

class Rule:
    def __init__(self,classification, value):
        self.classification = classification
        self.value = value

class NilaiFuzzyfication:
    def __init__(self, inputCode, classification, value):
        self.inputCode = inputCode
        self.classification = classification
        self.value = value

def fuzzyRule(emosi, provokasi):
    if (emosi=='Stabil'):
        if (provokasi=='Normal'):
            return 'Tidak'
        elif (provokasi=='Cukup Normal'):
            return 'Tidak'
        elif (provokasi=='Tidak Normal'):
            return 'Ya'
    elif (emosi=='Cukup Stabil'):
        if (provokasi=='Normal'):
            return 'Tidak'
        elif (provokasi=='Cukup Normal'):
            return 'Tidak'
        elif (provokasi=='Tidak Normal'):
            return 'Ya'
    elif (emosi=='Tidak Stabil'):
        if (provokasi=='Normal'):
            return 'Tidak'
        elif (provokasi=='Cukup Normal'):
            return 'Ya'
        elif (provokasi=='Tidak Normal'):
            return 'Ya'

def fuzzyfication(datastore,nEmosi, nProvokasi):
    if (nEmosi >= nStabilAwal and nEmosi <= nStabilAkhir):
        emosi0 = NilaiFuzzyfication('Emosi', 'Stabil', 1)
        datastore.append(emosi0);
    elif (nEmosi >= nCukupStabilAwal and nEmosi <= nCukupStabilAkhir):
        emosi0 = NilaiFuzzyfication('Emosi', 'Cukup Stabil', 1)
        datastore.append(emosi0);
    elif (nEmosi >= nTidakStabilAwal and nEmosi <= nTidakStabilAkhir):
        emosi0 = NilaiFuzzyfication('Emosi', 'Tidak Stabil', 1)
        datastore.append(emosi0);
    elif (nEmosi > nStabilAkhir and nEmosi < nCukupStabilAwal):
        valueEmosil = -1*(nEmosi - nCukupStabilAwal)/(nCukupStabilAwal-nStabilAkhir)
        emosi0 = NilaiFuzzyfication('Emosi', 'Stabil', valueEmosil)
        datastore.append(emosi0);

        valueEmosi2 = (nEmosi - nStabilAkhir) / (nCukupStabilAwal - nStabilAkhir)
        emosi1 = NilaiFuzzyfication('Emosi', 'Cukup Stabil', valueEmosi2)
        datastore.append(emosi1);
    elif (nEmosi > nCukupStabilAkhir and nEmosi < nTidakStabilAwal):
        valueEmosil = -1*(nEmosi - nTidakStabilAwal)/(nTidakStabilAwal-nCukupStabilAkhir)
        emosi0 = NilaiFuzzyfication('Emosi', 'Stabil', valueEmosil)
        datastore.append(emosi0);

        valueEmosi2 = (nEmosi - nCukupStabilAkhir) / (nTidakStabilAwal - nCukupStabilAkhir)
        emosi1 = NilaiFuzzyfication('Emosi', 'Cukup Stabil', valueEmosi2)
        datastore.append(emosi1);

    if (nProvokasi >= nNormalAwal and nProvokasi <= nNormalAkhir):
        provokasi0 = NilaiFuzzyfication('Provokasi', 'Normal', 1)
        datastore.append(provokasi0);
    elif (nProvokasi >= nCukupNormalAwal and nProvokasi <= nCukupNormalAkhir):
        provokasi0 = NilaiFuzzyfication('Provokasi', 'Cukup Normal', 1)
        datastore.append(provokasi0);
    elif (nProvokasi >= nTidakNormalAwal and nProvokasi <= nTidakNormalAkhir):
        provokasi0 = NilaiFuzzyfication('Provokasi', 'Tidak Normal', 1)
        datastore.append(provokasi0);
    elif (nProvokasi > nNormalAkhir and nProvokasi < nCukupNormalAwal):
        valueProvokasi0 = -1*(nProvokasi - nCukupNormalAwal) / (nCukupNormalAwal-nNormalAkhir)
        provokasi0 = NilaiFuzzyfication('Provokasi', 'Normal', valueProvokasi0)
        datastore.append(provokasi0);

        valueProvokasi1 = (nProvokasi - nNormalAkhir) / (nCukupNormalAwal - nNormalAkhir)
        provokasi1 = NilaiFuzzyfication('Provokasi', 'Cukup Normal', valueProvokasi1)
        datastore.append(provokasi1);
    elif (nProvokasi > nCukupNormalAkhir and nProvokasi < nTidakNormalAwal):
        valueProvokasi0 = -1 * (nProvokasi - nTidakNormalAwal) / (nTidakNormalAwal - nCukupNormalAkhir)
        provokasi0 = NilaiFuzzyfication('Provokasi', 'Cukup Normal', valueProvokasi0)
        datastore.append(provokasi0);

        valueProvokasi1 = (nProvokasi - nCukupNormalAkhir) / (nTidakNormalAwal - nCukupNormalAkhir)
        provokasi1 = NilaiFuzzyfication('Provokasi', 'Tidak Normal', valueProvokasi1)
        datastore.append(provokasi1);

def inference(datastore, rules):
    temp_rules = []
    for i in range (len(datastore)):
        if datastore[i].inputCode=='Emosi':
            for j in range(len(datastore)):
                if datastore[j].inputCode == 'Provokasi':
                    classification = fuzzyRule(datastore[i].classification,datastore[j].classification)
                    value = min(datastore[i].value,datastore[j].value)

                    print datastore[i].classification, datastore[j].classification, classification, value

                    rule0 = Rule(classification, value)
                    temp_rules.append(rule0)
    temp_rules.sort(key=lambda Rule: Rule.classification)
    rules.append(temp_rules[0])
    k = 0
    for i in range(len(temp_rules)):
        if (temp_rules[i].classification==rules[k].classification):
            if (temp_rules[i].value>rules[k].value):
                rules[k].value = temp_rules[i].value
        else:
            k+=1
            rules.append(temp_rules[i])

def defuzzyfication(rule):
    if (len(rule)==1):
        if (rule[0].classification=="Ya"):
            return rule[0].value * 25 / rule[0].value
        else:
            return rule[0].value * 75 / rule[0].value
    else:
        result = (rule[0].value*25 + rule[1].value*75)/(rule[0].value+rule[1].value)
        return result

if __name__=='__main__':
    datastore = []
    rules = []
    result = []
    nEmosi = 79
    nProvokasi = 81

    fuzzyfication(datastore,nEmosi,nProvokasi)
    for i in range(len(datastore)):
        print datastore[i].inputCode, datastore[i].classification, datastore[i].value
    print

    inference(datastore, rules)
    print

    if (defuzzyfication(rules)<=50):
        print "Ya"
    else:
        print "Tidak"
