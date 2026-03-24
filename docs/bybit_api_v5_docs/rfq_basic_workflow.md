# Basic Workflow

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/basic-workflow

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Basic Workflow



# Basic Workflow

**Basic concepts**

  1. Request for Quote (RFQ) – an inquiry sent by the inquiring party to the quoting party. The request for a quote includes one or more products and quantities that the inquiring party wishes to trade.
  2. Quote – provided in response to the inquiry. Sent by the quoting party to the inquiring party.
  3. Transaction – when the inquirer accepts and executes the quote.



**Basic workflow**

  1. The inquirier creates an RFQ and sends it to the quoters of their choice.
  2. Different quoting parties send quotes in response to this inquiry.
  3. The inquiring party chooses to execute the best quote to generate the transaction. The transaction executes and is settled.
  4. The inquiring party and the quoting party receive confirmation of the execution.
  5. The transaction details are published on the public market data channel (excluding party information).



**Creating an RFQ from the inquirer's perspective**

  1. The inquirer uses [/v5/rfq/create-rfq](https://bybit-exchange.github.io/docs/v5/rfq/trade/create-rfq) to create an inquiry. The inquirer can query the information of the products with [/v5/market/instruments-info](https://bybit-exchange.github.io/docs/v5/market/instrument), and the quoter information can be queried with [/v5/rfq/config query](https://bybit-exchange.github.io/docs/v5/rfq/trade/rfq-config).
  2. The inquirer may cancel the inquiry with [/v5/rfq/cancel-rfq](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-rfq) at any time while the inquiry is in force.
  3. The inquirer can use the endpoint [/v5/rfq/accept-other-quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/accept-other-quote) to accept non-LP OTC quotes, thereby expanding the sources of quotations.
  4. The quoting party, if it is one of the quoting parties selected by the inquiry party, will receive the inquiry information in the [rfq.open.rfqs](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/inquiry) WebSocket topic and can make the corresponding quote.
  5. The inquirer, after receiving the offer information in the [rfq.open.quotes](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/quote) WebSocket topic, can choose the best offer and execute it through the [/v5/rfq/execute-quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/execute-quote).
  6. Inquirers will receive confirmation of successful trade execution in the [rfq.open.trades](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/transaction) and [rfq.open.rfqs](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/inquiry) WebSocket topics.
  7. Inquirers will also receive confirmation of this and other block trades [rfq.open.public.trades](https://bybit-exchange.github.io/docs/v5/rfq/websocket/public/public-transaction) WebSocket topic.



**Creating a quote from the quoter's perspective**

  1. When a new request for a quote is issued and the quoting party is one of the selected quoting parties, the quoting party will receive this request information in the [rfq.open.rfqs](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/inquiry) WebSocket topic.
  2. The quoting party creates a quote and sends it via [/v5/rfq/create-quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/create-quote) .
  3. Quoters can cancel a valid quote at will with [/v5/rfq/cancel-quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-quote) .
  4. The inquiring party chooses to execute the optimal quote.
  5. Quoters receive status updates on their quotes via the [rfq.open.quotes](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/quote) WebSocket topic.
  6. Quoters will receive confirmation of the successful execution of their quote on the [rfq.open.trades](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/transaction) and [rfq.open.quotes](https://bybit-exchange.github.io/docs/v5/rfq/websocket/private/quote) WebSocket topics.
  7. The quoting party will also receive confirmation of this transaction and other block trades in the [rfq.open.public.trades](https://bybit-exchange.github.io/docs/v5/rfq/websocket/public/public-transaction) WebSocket topic.



[PreviousExecution](https://bybit-exchange.github.io/docs/v5/spread/websocket/private/execution)[NextCreate RFQ](https://bybit-exchange.github.io/docs/v5/rfq/trade/create-rfq)
