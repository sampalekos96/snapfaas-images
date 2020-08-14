mkfile_path := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: output.ext2

test:
	echo "apk add nodejs; node -e 'const app = require(\"./workload\"); app.handle({\"IP\": \"128.105.146.19\", \"PORT\": \"3456\", \"context\":{\"System\":{\"application\":{}}},\"request\":{\"locale\":\"en-US\",\"requestId\":\"amzn1.echo-external.request.5042db57-582e-4022-b070-4e4a769b29e1\",\"timestamp\":\"2020-08-13T23:26:29Z\",\"type\":\"LaunchRequest\"},\"version\":\"1.0\",\"session\":{\"application\":{},\"new\":true,\"sessionId\":\"SessionID.732dcba5-894a-49a6-bd31-0123e240ff0e\"}}, console.log);'" | docker run -i --rm -v $(mkfile_path):/srv -w /srv alpine:3.10

node_modules: package.json workload
	[ -d 'node_modules' ] && rm -r node_modules || true
	mkdir node_modules
	echo "apk add nodejs npm; npm install" | docker run -i --rm -v $(mkfile_path):/app -w /app alpine

output.ext2: ../.alexa-infra node_modules
	rm -rf output.ext2 /tmp/lorem.out/
	mkdir -p /tmp/lorem.out/
	touch output.ext2
	truncate -s 10M output.ext2
	mkfs.ext2 output.ext2
	sudo mount output.ext2 /tmp/lorem.out/
	sudo cp -r node_modules workload handler.js net.js ../.alexa-infra/language.js /tmp/lorem.out/
	sudo umount /tmp/lorem.out/
