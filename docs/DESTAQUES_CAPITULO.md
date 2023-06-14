# O que eu achei mais importante no capítulo Real-time data processing and analytics

### A diferença entre ingestão em tempo real e ingestão e processamento em tempo real

A ingestão em tempo real acontece quando um pipeline transmite dados, uma mensagem por vez, de uma origem para um destino. O processamento em tempo real se refere a transformações aplicadas em dados ingeridos em tempo real. Quando usar cada uma depende do produto.

A ingestão é usada quando é necessário disponibilizar dados para análises feitas por seres humanos. Mas é importante lembrar que os dados ingeridos não necessariamente serão consumidos em tempo real. Ela resolve problemas de dashboards “real time”.

A ingestão junto com processamento em tempo real são usados quando o produto requer que os dados ingeridos sejam disponibilizados para análises feitas por máquinas. É necessário considerar que usar DWs para processamento em tempo real é inviável, porque eles não são otimizados para resposta rápida, que é algo esperado de um produto real time. Esse tipo de sistema precisa ter um job de processamento, e os dados processados precisam ir para um armazenamento de baixa latência. Essa abordagem resolve problemas de sistemas de recomendação, detecção de fraudes, etc.
 

### Anatomia do fast storage

Os principais conceitos do fast storage são eventos, producers, consumers, tópicos. Os tópicos são replicados em partições dentro de clusters. Essas partições ficam dentro de brokers (máquinas) que tem seus próprios discos e armazenamentos locais. Eles são conectados em rede e agem juntos como um único cluster. As partições onde os tópicos são replicados contém eventos, que são registros de coisas que aconteceram. Para um evento ser salvo em um tópico, é necessário que um producer envie esse evento para o tópico. Uma vez no tópico, esse evento pode ser lido por um consumer.

Outros conceitos importantes são acknowledgments e offsets. Acknowledgments são notificações que o tópico envia quando um evento é gravado, isso serve para dizer ao producer que deu tudo certo com o evento e que ele pode enviar outro, se tiver. E offsets são identificadores atribuídos à mensagens quando são gravadas no tópico, isso ajuda o consumer a saber quais eventos ele já consumiu e quais falta consumir.
 

### Duplicação e deduplicação

Eventualmente acontecem problemas nos brokers e o fluxo descrito acima muda um pouco. Às vezes, por problemas de rede ou outros, um broker não consegue avisar ao producer que registrou o evento, e aí o producer envia o mesmo evento para o tópico. Nesse momento acontece duplicação. Outra forma de duplicação é quando os dados já chegam duplicados no tópico.

Algumas opções de deduplicação são Time window: juntar os dados por timestamp e identificar as duplicatas naquele time window; Id exclusivo: colocar IDs nos dados em um banco e consultar ele antes de enviar pro tópico; DW: deduplicações periódicas na tabela do dw.


### Referências complementares

* [Vídeo introdutório](https://youtu.be/B5j3uNBH8X4?list=PLa7VYi0yPIH2PelhRHoFR5iQgflg-y6JA) (porém não muito) que ajuda a entender o que tem dentro do cluster kafka
* [Playlist](https://www.youtube.com/playlist?list=PLa7VYi0yPIH2PelhRHoFR5iQgflg-y6JA) muito boa (com desenhos) sobre kafka
* Artigo de como era a [infra real time do Uber em 2021](https://arxiv.org/pdf/2104.00087.pdf) 
* Overview da [arquitetura do Pub/Sub](https://cloud.google.com/pubsub/architecture?hl=pt-br)
