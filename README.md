# 👨‍👩‍👧‍👦 Pesquisa Administração Pública - Bolsa Família

Este repositório contém os códigos e recursos desenvolvidos para o projeto de pesquisa que visa auxiliar a gestão do recurso financeiro do Bolsa Família utilizando técnicas de aprendizado de máquina.

![Static Badge](https://img.shields.io/badge/Status-Em_Desenvolvimento-blue)

## 🎯 Objetivo do Projeto

O objetivo deste projeto é desenvolver e avaliar um modelo de classificação que possa prever se uma família se enquadra como beneficiária do Bolsa Família com base em um conjunto de dados desindetificado com informações a respeito do Cadastro Único.

## 📝 Atividades Propostas

- [x] Coleta e organização dos dados
- [x] Pré-processamento dos dados
- [ ] Desenvolvimento de modelos de Machine Learning
  - [x] Random Forest
  - [x] Suport Vector Machine (SVM)
  - [x] K-Nearest Neighbors (KNN)
  - [ ] Recurrent Neural Networks (RNN)
  - [x] XGBoost
- [ ] Refatoração da limpeza dos dados
- [ ] Análise de impacto das melhores características

## 🗂️ Estrutura do Repositório

O repositório está dividido em pastas relacionadas as entregas solicitadas em cada etapa do projeto, seguindo a seguinte estruturação:

```
projeto-administracao-publica
├─ BolsaFamilia/
├─ CadUnico/
│  ├─ BasesCompletas/
│  ├─ BasesPB/
│  ├─ BasesRN/
│  ├─ BasesRNPB/
│  ├─ KNN/
│  │  ├─ TrainningPB.ipynb
│  │  └─ TrainningRN.ipynb
│  ├─ RandomForest/
│  │  ├─ TrainningPB.ipynb
│  │  └─ TrainningRN.ipynb
│  ├─ SVM/
│  │  ├─ TrainningPB.ipynb
│  │  └─ TrainningRN.ipynb
│  ├─ cadunico_2018.ipynb
│  └─ cadunico_2018.ipynb
├─ NovoBolsaFamiliaTransparencia/
├─ readme.md
└─ .gitignore
```

## 🚀 Tecnologias Utilizadas

As tecnologias utilizadas no projeto são as seguintes:

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable)

## 🛠️ Como utilizar

Para utilizar a aplicação siga esses passos:

- i. Clone o repositório:

  > git clone https://github.com/mariabandeira/AdministracaoPublica

- ii. Instale os pacotes necessários do Python:

  > pip install -r requirements.txt

- iii. Execute os Jupyters Notebooks.

## ⭐ Resultados

### 🤖 Técinicas de Machine Learning

Neste projeto, utilizamos diferentes algoritmos de Machine Learning para a predição de diabetes, avaliando sua performance em um conjunto de dados contendo atributos de saúde dos pacientes. As técnicas aplicadas incluem:

- Random Forest (RF): um modelo baseado em árvores de decisão que utiliza um conjunto de árvores para melhorar a precisão da predição e reduzir o overfitting;
- Support Vector Machine (SVM): algoritmo que busca um hiperplano ótimo para separar as classes no espaço de características, sendo eficaz especialmente para problemas com dados não linearmente separáveis;
- K-Nearest Neighbors (KNN): método baseado na proximidade entre os dados, classificando um novo ponto com base nas classes dos seus vizinhos mais próximos;
- XGBoost: uma técnica avançada de boosting que melhora a precisão e eficiência computacional, sendo amplamente utilizada para competições e aplicações do mundo real.

### 🐘 Resultados RN

#### Modelos treinados com todas as características

<table>
        <thead>
            <tr>
                <th rowspan="2">Modelo</th>
                <th rowspan="2">Acurácia</th>
                <th colspan="2">Precisão</th>
                <th colspan="2">Recall</th>
                <th colspan="2">F1-Score</th>
            </tr>
            <tr>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>KNN</td>
                <td>82%</td>
                <td>0.86</td>
                <td>0.79</td>
                <td>0.70</td>
                <td>0.91</td>
                <td>0.77</td>
                <td>0.84</td>
            </tr>
            <tr>
                <td>SVM</td>
                <td>89%</td>
                <td>0.91</td>
                <td>0.87</td>
                <td>0.82</td>
                <td>0.94</td>
                <td>0.86</td>
                <td>0.90</td>
            </tr>
            <tr>
                <td>RF</td>
                <td>90%</td>
                <td>0.94</td>
                <td>0.87</td>
                <td>0.82</td>
                <td>0.96</td>
                <td>0.87</td>
                <td>0.91</td>
            </tr>
            <tr>
                <td>XGBoost</td>
                <td>90%</td>
                <td>0.93</td>
                <td>0.88</td>
                <td>0.83</td>
                <td>0.95</td>
                <td>0.97</td>
                <td>0.91</td>
            </tr>
        </tbody>
</table>

#### Modelos treinados com as melhores características

<table>
        <thead>
            <tr>
                <th rowspan="2">Modelo</th>
                <th rowspan="2">Acurácia</th>
                <th colspan="2">Precisão</th>
                <th colspan="2">Recall</th>
                <th colspan="2">F1-Score</th>
            </tr>
            <tr>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>KNN</td>
                <td>83%</td>
                <td>0.81</td>
                <td>0.75</td>
                <td>0.82</td>
                <td>0.84</td>
                <td>0.82</td>
                <td>0.85</td>
            </tr>
            <tr>
                <td>SVM</td>
                <td>89%</td>
                <td>0.93</td>
                <td>0.86</td>
                <td>0.80</td>
                <td>0.96</td>
                <td>0.86</td>
                <td>0.91</td>
            </tr>
            <tr>
                <td>RF</td>
                <td>90%</td>
                <td>0.93</td>
                <td>0.88</td>
                <td>0.82</td>
                <td>0.96</td>
                <td>0.87</td>
                <td>0.91</td>
            </tr>
            <tr>
                <td>XGBoost</td>
                <td>90%</td>
                <td>0.93</td>
                <td>0.88</td>
                <td>0.82</td>
                <td>0.95</td>
                <td>0.87</td>
                <td>0.91</td>
            </tr>
        </tbody>
</table>

### 🦈 Resultados PB

#### Modelos treinados com todas as características

<table>
        <thead>
            <tr>
                <th rowspan="2">Modelo</th>
                <th rowspan="2">Acurácia</th>
                <th colspan="2">Precisão</th>
                <th colspan="2">Recall</th>
                <th colspan="2">F1-Score</th>
            </tr>
            <tr>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>KNN</td>
                <td>87%</td>
                <td>0.87</td>
                <td>0.87</td>
                <td>0.74</td>
                <td>0.94</td>
                <td>0.80</td>
                <td>0.90</td>
            </tr>
            <tr>
                <td>SVM</td>
                <td>90%</td>
                <td>0.91</td>
                <td>0.90</td>
                <td>0.80</td>
                <td>0.96</td>
                <td>0.85</td>
                <td>0.93</td>
            </tr>
            <tr>
                <td>RF</td>
                <td>91%</td>
                <td>0.94</td>
                <td>0.89</td>
                <td>0.78</td>
                <td>0.97</td>
                <td>0.85</td>
                <td>0.93</td>
            </tr>
            <tr>
                <td>XGBoost</td>
                <td>87%</td>
                <td>0.87</td>
                <td>0.86</td>
                <td>0.77</td>
                <td>0.93</td>
                <td>0.82</td>
                <td>0.90</td>
            </tr>
        </tbody>
</table>

#### Modelos treinados com as melhores características

<table>
        <thead>
            <tr>
                <th rowspan="2">Modelo</th>
                <th rowspan="2">Acurácia</th>
                <th colspan="2">Precisão</th>
                <th colspan="2">Recall</th>
                <th colspan="2">F1-Score</th>
            </tr>
            <tr>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
                <th>Classe 0</th>
                <th>Classe 1</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>KNN</td>
                <td>70%</td>
                <td>0.54</td>
                <td>0.92</td>
                <td>0.90</td>
                <td>0.58</td>
                <td>0.68</td>
                <td>0.71</td>
            </tr>
            <tr>
                <td>SVM</td>
                <td>90%</td>
                <td>0.93</td>
                <td>0.89</td>
                <td>0.78</td>
                <td>0.97</td>
                <td>0.85</td>
                <td>0.93</td>
            </tr>
            <tr>
                <td>RF</td>
                <td>90%</td>
                <td>0.92</td>
                <td>0.89</td>
                <td>0.79</td>
                <td>0.96</td>
                <td>0.85</td>
                <td>0.93</td>
            </tr>
            <tr>
                <td>XGBoost</td>
                <td>87%</td>
                <td>0.88</td>
                <td>0.86</td>
                <td>0.76</td>
                <td>0.93</td>
                <td>0.82</td>
                <td>0.90</td>
            </tr>
        </tbody>
</table>

## 👥 Equipe do Projeto

#### Discentes

- Luiz Fernando da Cunha Silva (UFERSA)
- Maria Eduarda Bandeira (UFPB)

#### Docentes Orientadoras

- Prof. Dra. Samara Martins Nascimento (UFERSA)
- Prof. Dra. Verônica Maria Lima Silva (UFPB)
