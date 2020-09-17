
package bin;

import java.net.*;
import java.io.*;
import java.lang.reflect.Method;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import edu.princeton.sns.VSock;

public class runtime_workload {

    private static int SERVER_PORT = 1234;
    private static int VMADDR_CID_HOST = 2;

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

	    /* for language snapshot */
        int cores = Runtime.getRuntime().availableProcessors();
        try {
            Process[] proc_list = new Process[cores];
            for (int i=1; i<cores; i++) {
                proc_list[i] = Runtime.getRuntime().exec(String.format("taskset -c %d outl 124 0x3f0", i));
            }
            proc_list[0] = Runtime.getRuntime().exec("taskset -c 0 outl 124 0x3f0");
            int exitVal = proc_list[0].waitFor();
            assert  exitVal == 0: "Err in enabling language snapshot";
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }

        /* mount appfs */
	    try {
            Process process = Runtime.getRuntime().exec("mount -r /dev/vdb /srv");
            int exitVal = process.waitFor();
            assert  exitVal == 0: "Err in mounting appfs";
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }

        /* load application */
        File file = null;
        ClassLoader cl = null;
        Class cls = null;
        Object o = null;
        Method app = null;

        try {
            file = new File("/");
            URL url = file.toURI().toURL();
            URL[] urls = new URL[]{url};
            cl = new URLClassLoader(urls);
            cls = cl.loadClass("srv.workload"); 

            o = cls.getDeclaredConstructor().newInstance();
            app = cls.getDeclaredMethod("handle", JSONObject.class);
            app.setAccessible(true);

        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }
	
	    /* load application jar dependecies */
	    File pkg_names = new File("/srv/package");
        try {
            if (pkg_names.length() > 0) {
                for (String pkg: pkg_names.list()) {
                    if (pkg.endsWith(".jar")) {
                        pkg = "/srv/package/"+pkg;
                        // System.out.println(pkg);
                        addJar(new File(pkg).toURI().toURL());
                    }
                }
            }
        }
        catch (Exception e) {
            System.out.println(e.getCause());
            System.exit(-1);
        }

        /* for function diff snapshot */
        try {
            Process[] proc_list = new Process[cores];
            for (int i=1; i<cores; i++) {
                proc_list[i] = Runtime.getRuntime().exec(String.format("taskset -c %d outl 124 0x3f0", i));
            }
            proc_list[0] = Runtime.getRuntime().exec("taskset -c 0 outl 124 0x3f0");
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
        // receive and execute requests from host until "end" is received
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
                if (req_json.get("request").equals("end")) {
                    // close connection
                    vsock.vsockClose();
                    break;
                }
            }
            catch(Exception e){
                System.out.println(e.getCause());
                break;
            }
        }
    }
}
