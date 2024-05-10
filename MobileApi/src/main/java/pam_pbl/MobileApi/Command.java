package pam_pbl.MobileApi;

import org.springframework.data.mongodb.core.mapping.Document;

@Document("commands")
public class Command {
    private String _id;
    private String user;
    private boolean lights;
    private boolean heating;

    public Command (String user, boolean lights, boolean heating){
        this.user = user;
        this.lights = lights;
        this.heating = heating;
    }

    public boolean isLights() {
        return lights;
    }

    public void setLights(boolean lights) {
        this.lights = lights;
    }

    public boolean isHeating() {
        return heating;
    }

    public void setHeating(boolean heating) {
        this.heating = heating;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }
}
