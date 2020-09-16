
package srv;

import org.json.simple.JSONObject;

public class workload {

    public workload() {

    }

    // hello
    public JSONObject handle(JSONObject req) {

        JSONObject obj = new JSONObject();

        obj.put("body", "hello world!");
        return obj;
    }

}
