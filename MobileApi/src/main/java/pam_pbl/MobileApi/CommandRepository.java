package pam_pbl.MobileApi;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface CommandRepository extends MongoRepository<Command, String> {

    @Query("{user:'?0'}")
    Command getCommand(String user);

}
