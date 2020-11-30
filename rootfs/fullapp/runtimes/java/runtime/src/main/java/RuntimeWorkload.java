import java.net.*;
import java.io.*;
import java.lang.reflect.Method;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import edu.princeton.sns.VSock;

public class RuntimeWorkload {

    private static final int SERVER_PORT = 1234;
    private static final int VMADDR_CID_HOST = 2;

    public static void addJar(URL url) throws Exception {

        URLClassLoader classLoader
                = (URLClassLoader) ClassLoader.getSystemClassLoader();
        Class clazz= URLClassLoader.class;

        // Use reflection
        Method method= clazz.getDeclaredMethod("addURL", new Class[] { URL.class });
        method.setAccessible(true);
        method.invoke(classLoader, new Object[] { url });
    }
    
    public static void main(String[] argv) {

        /* load application */
        File file = null;
        ClassLoader cl = null;
        Class cls = null;
        Object o = null;
        Method app = null;

        try {
            // first, add the dependency jar to classpath
            addJar(new File("/srv/libworkload.jar").toURI().toURL());

            file = new File("/");
            URL url = file.toURI().toURL();
            URL[] urls = new URL[]{url};
            cl = new URLClassLoader(urls);
            cls = cl.loadClass("srv.workload"); 

            // load the handle function in srv.workload
            o = cls.getDeclaredConstructor().newInstance();
            app = cls.getDeclaredMethod("handle", JSONObject.class);
            app.setAccessible(true);
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }

        // /* load application */
        // workload app = new workload();

        /* for function diff snapshot */
        int cores = Runtime.getRuntime().availableProcessors();
        try {
            Process[] proc_list = new Process[cores];
            for (int i=1; i<cores; i++) {
                proc_list[i] = Runtime.getRuntime().exec(String.format("taskset -c %d do-snapshot 123", i));
            }
            proc_list[0] = Runtime.getRuntime().exec("taskset -c 0 do-snapshot 123");
            int exitVal = proc_list[0].waitFor();
            assert  exitVal == 0: "Err in enabling function diff snapshot";
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }

        /* connect to host */
        VSock vsock = null;
        try {
            vsock = new VSock(VMADDR_CID_HOST, SERVER_PORT);
        }
        catch (IOException e) {
            System.out.println(e);
            System.exit(1);
        }

        JSONParser parser = new JSONParser();
        while (true)
        {
            try{
                String req_str = vsock.vsockRead();
                JSONObject req_json = (JSONObject) parser.parse(req_str);

                long start_time = System.nanoTime();
                JSONObject ret_json = (JSONObject) app.invoke(o, req_json);
                long end_time = System.nanoTime();

                ret_json.put("duration", end_time-start_time);
                vsock.vsockWrite(ret_json.toString());
            }
            catch(Exception e){
                System.out.println(e.getCause());
                break;
            }
        }
    }
}
