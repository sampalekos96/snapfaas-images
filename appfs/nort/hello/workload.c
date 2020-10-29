#include <string.h>
#include <inttypes.h>

void init() {
  return;
}

typedef void responder(char*, uint32_t);

void handle(char *request, uint32_t len, responder respond) {
  static char *payload = "{\"body\": \"hello, world!\"}";
  len = strlen(payload);
  respond(payload, len);
}
