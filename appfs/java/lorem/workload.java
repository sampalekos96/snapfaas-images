
package srv;

import org.json.simple.JSONObject;
import com.thedeanda.lorem.LoremIpsum;

public class workload {

    public workload() {

    }

    // lorem
    public JSONObject handle(JSONObject req) {

        JSONObject obj = new JSONObject();
        LoremIpsum ipsum = new LoremIpsum();

        obj.put("body", ipsum.getWords(6, 12));
        return obj;
    }

}
