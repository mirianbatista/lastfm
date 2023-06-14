# Arquitetura Lastfm Mírian

Em resumo, 21 vezes por minuto é feito um request para a API do Lastfm, os dados recebidos são enviados para um tópico Pub/Sub, existe um subcriber que envia os dados do tópico para o BigQuery, e o Streamlit faz queries no BigQuery para mostrar o resultado mais recente (ou seja, a música que estou ouvindo naquele momento). Na imagem abaixo podemos observar como isso acontece:

<img
  src="https://github.com/mirianbatista/lastfm/blob/main/docs/arq_lastfm.png"
  alt="Arquitetura Lastfm Mírian">

Agora que temos uma visão geral, vamos ver detalhadamente o que acontece em cada momento.

### Request Lastfm e envio dos dados para o tópico Pub/Sub

A primeira parte do processo acontece no Airflow. Essa ferramenta foi escolhida pelos recursos nativos que facilitam o desenvolvimento, e também pela facilidade de orquestração e monitoramento. A quantidade de 21 execuções por minuto foi o que se mostrou o valor ótimo para que a maior quantidade possível de requests fossem feitas sem sobrecarregar a API do Lastfm nem o Airflow. 

No código, a request pega as músicas mais recentes, e em seguida a música mais recente é filtrada, convertida em bytes (formato requisitado pelo Pub/Sub) e enviada para o tópico Pub/Sub através do operator Airflow PubSubPublishMessageOperator.

### Pub/Sub, BigQuery e Lastfm

Foi configurado na UI da GCP um subscriber para quando chegar dados no tópico, ele enviar para uma tabela no BigQuery. Essa tabela tem retenção de 1h.

No Streamlit, a cada 2 segundos é feita uma query para pegar o valor mais recente da tabela BigQuery alimentada pelo subscriber descrito acima. O resultado é colocado em um dicionário e exibido no formato definido no markdown.
