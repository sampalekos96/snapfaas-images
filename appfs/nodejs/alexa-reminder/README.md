port from: https://github.com/alexa/skill-sample-nodejs-fact

### Example Request
1. AddItemIntent
```json
{
  "DATABASE":"reminders",
  "COUCHDB_URL":"http://admin:admin@128.105.145.79:5984",
  "context":{
    "System":{"application":{}}},
    "request":{
      "locale":"en-US",
      "requestId":"amzn1.echo-external.request.5042db57-582e-4022-b070-4e4a769b29e1",
      "timestamp":"2020-08-13T23:26:29Z",
      "type":"IntentRequest",
      "intent":{
        "name":"AddItemIntent",
        "slots":{
          "place":{"value":"kitchen"},
          "item":{"value":"buy more milk"}
        }
      }
   },
   "version":"1.0",
   "session":{"application":{},"new":true,"sessionId":"SessionID.732dcba5-894a-49a6-bd31-0123e240ff0e"}
}
```
Related fields: `DATABASE`, `COUCHDB_URL`, `request.intent.name`, `request.intent.slots.place.value`, `request.intent.slots.item.value`.

2. RetrieveItemIntent
```json
{
  "DATABASE":"reminders",
  "COUCHDB_URL":"http://admin:admin@128.105.145.79:5984",
  "context":{
    "System":{"application":{}}},
    "request":{
      "locale":"en-US",
      "requestId":"amzn1.echo-external.request.5042db57-582e-4022-b070-4e4a769b29e1",
      "timestamp":"2020-08-13T23:26:29Z",
      "type":"IntentRequest",
      "intent":{
        "name":"RetrieveItemIntent",
        "slots":{
          "place":{"value":"kitchen"},
        }
      }
   },
   "version":"1.0",
   "session":{"application":{},"new":true,"sessionId":"SessionID.732dcba5-894a-49a6-bd31-0123e240ff0e"}
}
```
Related fields: `DATABASE`, `COUCHDB_URL`, `request.intent.name`, `request.intent.slots.place.value`.
