import numpy as np
import matplotlib.pyplot as plt

#Määritetään funktio, joka laskee liukuvan keskiarvon datasta
def liukuva_keskiarvo(data, n):
    liukuva_lista = np.array([])
    i = 0
    askel = int(n/2)
    while i < len(data):
        if i - askel < 0:
            ikkuna = data[0: i + askel + 1]
            ikkuna_arvo = sum(ikkuna) / np.size(ikkuna)
            liukuva_lista = np.append(liukuva_lista, ikkuna_arvo)
        elif len(data)-askel <= i:
            ikkuna = data[i-askel: ]
            ikkuna_arvo = sum(ikkuna) / np.size(ikkuna)
            liukuva_lista = np.append(liukuva_lista, ikkuna_arvo)
        else:
            ikkuna = data[i-askel: i + askel+1]
            ikkuna_arvo = sum(ikkuna) / n
            liukuva_lista = np.append(liukuva_lista, ikkuna_arvo)
        i += 1
    return liukuva_lista

#Määritetään funktio, joka laskee symmetrisen derivaatan datasta
def derivaatta (x, y):
    derivaatat = np.array([])
    derivaatat = np.append(derivaatat, np.nan) #Listan ensimmäinen elementti on nan
    i=1
    while i < len(x)-1:
        deriv = (y[i+1]-y[i-1])/(x[i+1]-x[i-1])
        derivaatat = np.append(derivaatat, deriv)
        i += 1
    derivaatat = np.append(derivaatat, np.nan)  # Listan viimeinen elementti on nan
    return derivaatat

#Luetaan datatiedosto ja tallenetaan sarakkeet muuttujiin:
data = np.loadtxt("measurement_data.dat")
aika = data[:,0]
pienhiukkaspitoisuus = data[:,1]
havionopeus = data[:,2]
rikkihappopitoisuus = data[:,3]
orgaaninenpitoisuus = data[:,4]

#Määritetään datasta painotetut keskiarvot kohinan poistamiseksi:
hiukkaset_keskiarvo = liukuva_keskiarvo(pienhiukkaspitoisuus, 5)
rikkihapon_keskiarvo = liukuva_keskiarvo(rikkihappopitoisuus, 5)
orgaaninen_keskiarvo = liukuva_keskiarvo(orgaaninenpitoisuus, 5)

#Piirretään kuvaajat pitoisuuksista:
fig1, ax = plt.subplots(3,1)
ax[0].semilogy(aika,hiukkaset_keskiarvo,)
ax[1].semilogy(aika,rikkihapon_keskiarvo)
ax[2].semilogy(aika,orgaaninen_keskiarvo)
ax[0].set_xlim(0, 120)
ax[1].set_xlim(0, 120)
ax[2].set_xlim(0,120)
ax[0].set_xlabel("Aika (h)")
ax[1].set_xlabel("Aika (h)")
ax[2].set_xlabel("Aika (h)")
ax[0].set_title("Keskiarvoistettu hiukkaspitoisuus")
ax[1].set_title("Keskiarvoistettu rikkihappopitoisuus")
ax[2].set_title("Keskiarvoistettu orgaanisten yhdisteiden pitoisuus")
ax[0].set_ylabel("Hiukkasia/cm^3")
ax[1].set_ylabel("Molekyyliä/cm^3")
ax[2].set_ylabel("Molekyyliä/cm^3")
fig1.tight_layout()

#Piirretään kuvaaja, jossa näkyy keskiarvoistamaton ja keskiarvoistettu hiukkaspitoisuus:
fig2 = plt.figure()
plt.plot(aika, pienhiukkaspitoisuus, label = "Keskiarvoistamaton hiukkaspitoisuus")
plt.plot(aika, hiukkaset_keskiarvo, label = "Keskiarvoistettu hiukkaspitoisuus")
plt.xlim(75,78)
plt.ylim(0,175)
plt.title("Hiukkaspitoisuus ajan funktiona")
plt.xlabel("Aika (h)")
plt.ylabel("Hiukkasia/cm^3")
plt.legend()


# #Määritetään hiukkasten muodostumisnopeus:
pitoisuus_derivaatta = derivaatta(aika*60*60, hiukkaset_keskiarvo) #Muutettu sekunneiksi
muodostumisnopeus = pitoisuus_derivaatta + havionopeus

#Piirretään muodostumisnopeudesta kuvaajia:
fig3 = plt.figure()
plt.loglog(rikkihapon_keskiarvo, muodostumisnopeus, "o")
plt.xlabel("Rikkihappopitoisuus (molekyyliä/cm^3)")
plt.ylabel("Hiukkasten muodostumisnopeus (1/cm^3/s)")
plt.title("Muodostumisnopeus rikkihappopitoisuuden funktiona")

fig4 = plt.figure()
plt.loglog(orgaaninen_keskiarvo, muodostumisnopeus, "ro")
plt.xlabel("Orgaanisten yhdisteiden pitoisuus (molekyyliä/cm^3)")
plt.ylabel("Hiukkasten muodostumisnopeus (1/cm^3/s)")
plt.title("Muodostumisnopeus orgaanisten yhdisteiden pitoisuuden funktiona")

fig5 = plt.figure()
plt.loglog(rikkihapon_keskiarvo*orgaaninen_keskiarvo, muodostumisnopeus, "go")
plt.xlabel("Rikkihappopitoisuus * orgaanisten yhdisteiden pitoisuus (molekyyliä/cm^3)")
plt.ylabel("Hiukkasten muodostumisnopeus (1/cm^3/s)")
plt.title("Muodostumisnopeus rikkihappopitoisuuden ja orgaanisten yhdisteiden pitoisuuden tulona funktiona")

#Määritetään steady-state -jaksoja vastaavat keskiarvot
steady_data = np.loadtxt("experiment_steady.dat")
steady_nopeus = np.array([])
steady_rikkihappo = np.array([])
steady_orgaaninen = np.array([])

for jakso in steady_data:
    j=0
    jakso_nopeus = np.array([])
    jakso_rikki = np.array([])
    jakso_orgaaninen = np.array([])
    while j < len(aika):
        if jakso[0] < aika[j] < jakso[1]:
            jakso_nopeus = np.append(jakso_nopeus, muodostumisnopeus[j])
            jakso_rikki = np.append(jakso_rikki, rikkihapon_keskiarvo[j])
            jakso_orgaaninen = np.append(jakso_orgaaninen, orgaaninen_keskiarvo[j])
        j += 1
    steady_nopeus = np.append(steady_nopeus, np.nanmean(jakso_nopeus))
    steady_rikkihappo = np.append(steady_rikkihappo, np.nanmean(jakso_rikki))
    steady_orgaaninen = np.append(steady_orgaaninen, np.nanmean(jakso_orgaaninen))

#Piirretään steady-state -keskiarvoista kuvaaja:

fig6 = plt.figure()
plt.loglog(steady_rikkihappo * steady_orgaaninen, steady_nopeus, "ko", label = "Datapisteet")
plt.xlabel("Rikkihappopitoisuus * orgaanisten yhdisteiden pitoisuus (molekyyliä/cm^3)")
plt.ylabel("Hiukkasten muodostumisnopeus (1/cm^3/s)")
plt.title("Muodostumisnopeus rikkihappopitoisuuden ja orgaanisten yhdisteiden pitoisuuden tulona funktiona (steady-state -keskiarvot)")

#Sovitetaan pisteisiin suora:
x = np.log10(steady_orgaaninen * steady_rikkihappo)
y = np.log10(steady_nopeus)
params = np.polyfit(x, y, 1)
xx = np.logspace(np.min(x), np.max(x), 50)
yy = 10**params[1] * xx**params[0]
plt.plot(xx, yy, color ="#FFA500", linewidth = 5, label = "Sovitus")
plt.legend()

plt.show()
