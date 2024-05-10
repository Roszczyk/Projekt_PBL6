package pam_pbl.MobileApi;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class })
public class MobileApi {
//	private final static Logger logger = LoggerFactory.getLogger(MobileApi.class);

	public static void main(String[] args) {
		SpringApplication.run(MobileApi.class, args);
	}
}
 	