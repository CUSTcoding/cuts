# Sistema de Gestão de Barbearia

## Documentação

[Como configurar e ativar o ambiente virtual](docs/readme.md#ativar-o-ambiente-virtual)

## Sobre o projeto

Quero criar um sistema para ajudar a gerir uma barbearia de forma mais organizada.

Atualmente, uma parte importante do funcionamento da barbearia depende de processos manuais. Os clientes precisam entrar em contacto com a barbearia para marcar um horário, os atendimentos precisam ser organizados, os barbeiros precisam saber quem será atendido a seguir e a administração precisa acompanhar o que está acontecendo no negócio.

A ideia é transformar esses processos em um sistema único.

O sistema deverá ser utilizado pelos **clientes, barbeiros e responsáveis pela administração da barbearia**.

Não quero definir antecipadamente como o sistema deverá ser construído. A responsabilidade do desenvolvedor será entender o funcionamento descrito abaixo, analisar o problema e decidir como transformar essas necessidades em uma solução de software.

---

# Como imagino a experiência do cliente

Quero que uma pessoa possa utilizar a barbearia sem necessariamente precisar criar uma conta.

Por exemplo, uma pessoa pode entrar no sistema, escolher o serviço que deseja realizar e marcar um horário informando pelo menos o seu nome e número de telefone.

Depois de marcar, deverá receber alguma forma de identificação do seu atendimento.

Essa identificação deverá permitir que a barbearia encontre facilmente o agendamento quando o cliente chegar.

Por outro lado, quem utiliza a barbearia frequentemente poderá criar uma conta.

Na conta, quero que o cliente possa fornecer informações como:

* Nome;
* Número de telefone;
* Email;
* Username;
* Palavra-passe.

Depois de possuir uma conta, o cliente deverá conseguir acompanhar melhor a sua relação com a barbearia.

Por exemplo, deverá conseguir consultar os seus agendamentos, histórico de atendimentos, bônus acumulados e outras informações relacionadas à sua utilização do serviço.

---

# Agendamentos

Quero que o cliente consiga marcar um atendimento sem precisar telefonar ou falar diretamente com alguém da barbearia.

Ele deverá conseguir escolher o serviço que deseja realizar e encontrar um horário disponível.

Dependendo de como o sistema for projetado, também poderá escolher um barbeiro específico.

Depois de realizar a marcação, o sistema deverá guardar as informações necessárias para que a barbearia saiba:

* Quem é o cliente;
* O que ele pretende fazer;
* Quando deverá ser atendido;
* Qual barbeiro poderá atendê-lo;
* Qual é a situação atual daquele agendamento.

O cliente também deverá poder consultar o seu agendamento posteriormente.

Deverá existir uma forma de lidar com situações como cancelamentos, alterações de horário, atrasos e clientes que simplesmente não aparecem.

Essas situações deverão ser analisadas e definidas durante o desenvolvimento.

---

# Identificação do atendimento

Quando alguém marca um atendimento, quero que o sistema gere uma identificação para esse atendimento.

Imagino algo parecido com um **ticket digital**.

Esse ticket deverá conter informações suficientes para identificar o atendimento e deverá possuir também um **QR Code**.

Quando o cliente chegar à barbearia, poderá apresentar esse QR Code para confirmar que chegou.

Também quero que exista uma alternativa para situações em que o cliente não consiga apresentar o QR Code.

Por exemplo, um funcionário poderá procurar o atendimento utilizando o nome, número de telefone ou outra informação que permita encontrar o cliente.

---

# Chegada do cliente à barbearia

Quando o cliente chegar, quero que o sistema consiga registrar que ele realmente está na barbearia.

Depois disso, ele deverá entrar no processo de atendimento.

A partir desse momento, a barbearia deverá conseguir saber quem está esperando, quem já foi chamado, quem está sendo atendido e quem já terminou.

---

# Fila de atendimento

Uma das partes mais importantes do sistema será a gestão da fila.

Imagine que existam quatro pessoas esperando:

```text
1 — João
2 — Maria
3 — Carlos
4 — Pedro
```

O barbeiro deverá conseguir chamar o próximo cliente.

Mas existe um problema.

Imagine que Maria seja chamada e não esteja presente.

Não quero que a ausência dela bloqueie o atendimento das outras pessoas.

Nesse caso, o próximo cliente deverá poder ser chamado.

Por exemplo:

```text
João    → esperando
Maria   → não apareceu
Carlos  → próximo
Pedro   → esperando
```

Se Carlos for atendido, Pedro poderá ser chamado depois.

O sistema deverá manter a informação sobre o que aconteceu com Maria.

Também deverá existir uma forma de tratar o caso em que Maria aparece posteriormente.

A regra exata para esse tipo de situação deverá ser analisada e definida pelo desenvolvedor de acordo com uma solução coerente para o negócio.

---

# Barbeiros

A barbearia possui vários barbeiros.

Quero conseguir cadastrar e administrar esses profissionais dentro do sistema.

Cada barbeiro deverá ter informações próprias e deverá ser possível saber quando ele está disponível para atender.

O barbeiro deverá conseguir visualizar os clientes que precisa atender e informar ao sistema quando começa e termina um atendimento.

Também quero que seja possível saber o histórico de atendimentos realizados por cada barbeiro.

Caso existam vários barbeiros atendendo ao mesmo tempo, o sistema deverá conseguir lidar corretamente com essa situação.

---

# Serviços

A barbearia oferece diferentes serviços.

Por exemplo:

* Corte de cabelo;
* Barba;
* Corte + barba;
* Outros serviços que possam ser adicionados posteriormente.

Quero conseguir cadastrar novos serviços, alterar informações e definir os respetivos preços.

O sistema deverá considerar também o tempo necessário para realizar cada serviço, porque isso influencia diretamente os horários disponíveis para agendamento.

---

# Pagamento

Depois de um atendimento, o cliente deverá realizar o pagamento.

O sistema deverá guardar informações suficientes para saber quanto foi pago e qual serviço ou serviços foram realizados.

A solução deverá ser preparada para permitir diferentes formas de pagamento, caso a barbearia decida adicionar novos métodos no futuro.

---

# Programa de bônus

Quero criar um sistema para incentivar os clientes a continuarem utilizando a barbearia.

A ideia é que, quando um cliente realizar um corte ou outra operação elegível, ele receba um bônus equivalente a **2% do valor pago**, de acordo com as regras definidas pela barbearia.

Por exemplo:

Se um cliente pagar:

```text
500 MZN
```

Ele poderá receber:

```text
10 MZN
```

em bônus.

Esse bônus deverá ficar associado ao cliente.

Se posteriormente ele acumular vários bônus, poderá utilizá-los para obter desconto ou pagar um atendimento, conforme as regras estabelecidas.

Por exemplo:

```text
Bônus acumulado: 150 MZN

Valor do próximo corte: 500 MZN
```

O cliente poderá utilizar os 150 MZN e pagar o restante, caso essa seja uma das regras permitidas.

Também quero conseguir saber de onde veio cada bônus e quando ele foi utilizado.

O sistema deverá evitar situações em que bônus sejam criados ou utilizados indevidamente.

---

# Produtos

Além dos serviços, a barbearia também poderá vender produtos.

Por exemplo:

* Pomadas;
* Óleos para barba;
* Shampoos;
* Pentes;
* Escovas;
* Produtos para cabelo;
* Outros produtos relacionados.

Quero que o administrador consiga cadastrar esses produtos, definir preços e controlar a quantidade disponível.

Os clientes deverão conseguir visualizar os produtos e realizar compras através do sistema.

---

# Compras

Quero que um cliente possa escolher vários produtos antes de finalizar uma compra.

Por isso, deverá existir algum conceito de carrinho.

Depois de finalizar a compra, a barbearia deverá conseguir acompanhar o pedido e saber em que situação ele se encontra.

Por exemplo, saber se o pedido ainda está aguardando pagamento, sendo preparado ou já foi entregue.

A forma exata como esse processo será implementado deverá ser definida pelo desenvolvedor.

---

# Avisos aos clientes

Quero que o sistema consiga avisar os clientes quando algo importante acontecer.

Por exemplo:

Um cliente possui um agendamento para amanhã.

O sistema poderá lembrá-lo.

Quando estiver próximo da vez dele, poderá receber outro aviso.

Quando chegar a sua vez, deverá receber uma notificação informando que pode ser atendido.

Também poderá receber uma notificação quando receber bônus ou quando houver alguma alteração importante no seu agendamento.

A solução deverá ser preparada para permitir esse tipo de comunicação.

---

# Administração

Preciso de uma área onde os responsáveis pela barbearia possam administrar o negócio.

Nessa área deverá ser possível, de alguma forma, gerir:

* Clientes;
* Barbeiros;
* Serviços;
* Agendamentos;
* Fila;
* Produtos;
* Pedidos;
* Bônus;
* Pagamentos;
* Outras informações importantes.

Também quero conseguir visualizar informações que ajudem a perceber como a barbearia está funcionando.

Por exemplo:

* Quantos clientes foram atendidos;
* Quantos agendamentos foram realizados;
* Quantos clientes não apareceram;
* Quais serviços são mais procurados;
* Quais produtos vendem mais;
* Quanto a barbearia faturou;
* Quanto foi concedido em bônus;
* Quais barbeiros realizaram mais atendimentos;
* Quais horários possuem maior movimento.

Não é necessário limitar a administração somente a esses dados. O desenvolvedor deverá analisar quais informações seriam úteis para a gestão do negócio.

---

# Segurança

O sistema terá informações pessoais dos clientes e informações relacionadas a pagamentos e atendimento.

Por isso, quero que a segurança seja considerada desde o início do projeto.

As palavras-passe dos clientes não podem ser armazenadas de forma que alguém consiga simplesmente visualizá-las no banco de dados.

Também quero que cada pessoa tenha acesso apenas às funcionalidades que correspondem ao seu papel.

Por exemplo, um cliente não deve possuir os mesmos privilégios de um administrador.

A solução deverá considerar também outras questões de segurança que o desenvolvedor identificar durante a análise.
