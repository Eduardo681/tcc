
# Uso da análise de dados em cenários empresariais: Incrementado à Estratégia de Marketing Digital

# Documentos finais
https://drive.google.com/drive/folders/1U9of3Xb72RIVhEc8GMs5yS1HMAbPTETh?usp=drive_link

# Introdução

O perfil do consumidor mudou com a disseminação da internet e redes sociais, a opinião sobre uma marca ou produto deixou
de levar em consideração somente o serviço oferecido, valorizando principalmente a experiência de uso e identificação
com a marca.

## Objetivos

Fornecer uma metodologia de acompanhamento das publicações de consumidores e oferecer um
relatório para profissionais de marketing e gestores, com a finalidade de colaborar com o processo estratégico de tomada
de decisão.

Utilizar de data mining e data science para buscar dados online e fornecer uma solução que permita à empresa uma
estratégia de tomada de decisões baseada em dados. Dessa forma, o presente trabalho irá executar a mineração de dados na
base do twitter e gerar um relatório que forneça dados para um profissional avaliar o posicionamento da marca e as
avaliações de consumidores.

## Dados

Os dados foram coletados a partir do twitter utilizando a biblioteca tweepy, utilizando o termo de busca 'IFood'. Abaixo
dicionario de dados resultante da mineração de dados:

| Coluna        | Tipo   | Descrição                                                                |
|---------------|--------|--------------------------------------------------------------------------|
| id            | int64  | Identificador único auto-incrementável                                   |
| user          | object | Nome do usuário que executou a publicação                                |
| id_tweet      | int64  | Identificador de publicação                                              |
| text          | object | Conteúdo textual da postagem                                             |
| created_at    | object | Data da publicação                                                       |
| retweet_count | int64  | Quantidade de compartilhamentos, não incluídos os com novos comentários. |
| reply_count   | int64  | Quantidade de comentários                                                |
| like_count    | int64  | Quantidades de gostei na publicação                                      |
| quote_count   | int64  | Quantidade de compartilhamentos com novos comentários                    |

# Etapas executadas

- Pré processamento -> Remoção de pontuação, Remoção de Dados Indesejados (duplicidade e colunas sem valor para análise)
  , tokenização, remoção de stopwords, lematização
- Matriz de Frequência de Termos
- WordClouds
- Modelo para análise de sentimentos

## Resultados
### Dashboard
#### Tela 01
![Screenshot from ![Screenshot from 2022-08-26 19-28-39](https://user-images.githubusercontent.com/50171354/186999054-9a0229ca-c778-410b-a49c-b4dc47693350.png)
2022-08-26 19-28-26](https://user-images.githubusercontent.com/50171354/186998874-29031580-35f2-48ba-b817-af82e0116236.png)

#### Tela 02
![Screenshot from 2022-08-26 19-28-39](https://user-images.githubusercontent.com/50171354/186999424-70943ac6-5264-44e3-a7da-6ec4588c852e.png)


### Analise
Em análise dos resultados obtidos com a o processo realizado utilizando a empresa IFood destaca-se os seguintes pontos:
- A porcentagem de comentários negativos é alta e filtrando nota-se que  que tal classificação está correlacionada principalmente com a falta de suporte em reembolsos e cancelamentos, bem como problemas na entrega;
- Nota-se que tem um alto número de compartilhamentos, comparando com os outros índices;
- As palavras entrega e entregador são constantes nas word clouds, demonstrando a importância desse processo para o sucesso do app; 
- A matriz de frequências e word clouds demonstram que as palavras cupom, valor, boleto são frequentes. Ao buscar por elas na base, é perceptível que valor e boleto está relacionado a muitas postagens relatando os altos gastos por comprar muito no aplicativo, enquanto há muita publicidade com a palavra cupom;
- Filtrando pelos dados positivos percebe-se que o uso do aplicativo para supermercado e farmácias vem crescendo e é destacado como algo positivo pelos usuários;
- Filtrando pelos dados negativos é perceptível a insatisfação dos usuários com a funcionalidade de pedido minimo para cupons;
