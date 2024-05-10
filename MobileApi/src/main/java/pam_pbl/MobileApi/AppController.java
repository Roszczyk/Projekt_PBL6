package pam_pbl.MobileApi;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Collections;
import java.util.Map;

@RestController
//@RequestMapping("/data")
public class AppController {

    @Autowired
    CommandRepository commandRepo;

    @PostMapping("/{user}/{path}")
    public ResponseEntity<Map<String, String>> handlePostRequest(
            @PathVariable String user,
            @PathVariable String path,
            @RequestParam("value") boolean value) {

        Command currCommand = commandRepo.getCommand(user);
        System.out.println(currCommand);

        if ("lights".equals(path)) {
            if (value != currCommand.isLights()){
                currCommand.setLights(value);
                commandRepo.save(currCommand);
                System.out.println("wyślij do Pub_Sub");
                return ResponseEntity.status(HttpStatus.CREATED).body(Collections.singletonMap("message", "OKK"));
            }
            else {
                return ResponseEntity.status(HttpStatus.NO_CONTENT).body(Collections.singletonMap("message", "Already raproted"));
            }
        } else if ("heating".equals(path)) {
            if (value != currCommand.isHeating()){
                currCommand.setHeating(value);
                commandRepo.save(currCommand);
                System.out.println("wyślij do Pub_Sub");
                return ResponseEntity.status(HttpStatus.CREATED).body(Collections.singletonMap("message", "OKK"));
            }
            else {
                return ResponseEntity.status(HttpStatus.NO_CONTENT).body(Collections.singletonMap("message", "Already raproted"));
            }
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Collections.singletonMap("message", "NO!"));
        }
    }
}
