package com.example.hive

import android.annotation.SuppressLint
import android.content.Intent
import android.os.AsyncTask
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.View
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.RelativeLayout
import android.widget.TextView
import com.android.volley.toolbox.JsonObjectRequest
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.Volley
import android.widget.Toast
import com.android.volley.AuthFailureError

class MainActivity : AppCompatActivity() {

    private lateinit var ValTemp: TextView
    private lateinit var ValHum: TextView
    private lateinit var ValOpen: TextView
    private lateinit var ValLight: TextView
    private lateinit var ValHeat:TextView
    private lateinit var ValUpdate: TextView
    private lateinit var ValNoise:TextView
    private lateinit var ValAtivity: TextView
    private lateinit var Name:TextView
    private lateinit var Logout:TextView
    private lateinit var BtnMap: LinearLayout
    private lateinit var BtnLight: LinearLayout
    private lateinit var BtnHeat: LinearLayout
    private lateinit var BtnHum: LinearLayout
    private lateinit var BtnTemp: LinearLayout
    private lateinit var progressBar: ProgressBar
    private lateinit var ImageLight: ImageView
    private lateinit var ImageHeat: ImageView
    private lateinit var ImageCover: ImageView
    private lateinit var ImageBack: ImageView
    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        ValTemp = findViewById(R.id.temperature)
        ValHum = findViewById(R.id.humidity)
        ValOpen = findViewById(R.id.openstatus)
        ValLight = findViewById(R.id.lightstatus)
        ValNoise = findViewById(R.id.noise)
        ValAtivity = findViewById(R.id.activity)
        ValHeat = findViewById(R.id.heatingstatus)
        ValUpdate = findViewById(R.id.updated_at)
        Name = findViewById(R.id.hiveName)
        Logout = findViewById(R.id.logout)
        ImageBack = findViewById(R.id.back)
        //progressBar = findViewById(R.id.loader)
        BtnMap = findViewById(R.id.boxMap)
        BtnHum = findViewById(R.id.boxhum)
        BtnLight = findViewById(R.id.boxlight)
        BtnHeat = findViewById(R.id.boxheat)
        BtnTemp = findViewById(R.id.boxTemp)
        ImageLight = findViewById(R.id.imglight)
        ImageHeat = findViewById(R.id.imgheat)
        ImageCover = findViewById(R.id.imgcover)
      //  progressBar.visibility = View.VISIBLE



        val baseUrl = "http://10.0.2.2:5000/"

        val hiveData = intent.getStringExtra("selectedHive")
        val password = intent.getStringExtra("password")
        val username = intent.getStringExtra("username")

        if (hiveData != null && username != null && password != null) {
            ApiCall().getsensor(this, hiveData,username, password) { payload ->
                var temp = payload.temperature.toString()
                var hum = payload.humidity.toString()
                var cover = payload.digital_in.toString()
                var heat = payload.heating.toString()
                var lig = payload.lights.toString()
                var noise = payload.noise.toString()
                var activity = payload.activity.toString()
                //TO DO when new version of payload NO GPS
                if (cover == "false") {
                    ValOpen.text = "open"
                    ImageCover.setImageResource(R.drawable.openclose)
                }
                else {
                    ValOpen.text = "closed"
                    ImageCover.setImageResource(R.drawable.close)
                }


                if (heat == "true") {
                    ValHeat.text = "ON"
                    ImageHeat.setImageResource(R.drawable.heatingon)
                }
                else{
                    ValHeat.text = "OFF"
                    ImageHeat.setImageResource(R.drawable.heating)
                }
                if (lig == "true") {
                    ValLight.text = "ON"
                    ImageLight.setImageResource(R.drawable.lighton)
                }
                else {
                    ValLight.text = "OFF"
                    ImageLight.setImageResource(R.drawable.light)
                }
                if (noise == "true") {
                    ValNoise.text = "high"
                }
                else {
                    ValNoise.text = "low"
                }
                if (activity == "true") {
                    ValAtivity.text = "high"
                }
                else {
                    ValAtivity.text = "low"
                }


                //to this line
                //Setting correct timestamp of update for last update
                val currentTimestamp = System.currentTimeMillis()
                val timeZone = TimeZone.getTimeZone("Europe/Warsaw")
                val dateFormat = SimpleDateFormat("dd MMM yyyy, HH:mm", Locale("pl", "PL"))

                dateFormat.timeZone = timeZone
                ValUpdate.text = dateFormat.format(Date(currentTimestamp))
                ValTemp.text = "$temp°C"
                ValHum.text = "$hum%"
                Name.text = "Hive no.  " + hiveData
                //progressBar.visibility = View.GONE

            }
        }

        BtnMap.setOnClickListener() {
            val intent = Intent(this, MapActivity::class.java)
            intent.putExtra("hiveData", hiveData)
            intent.putExtra("password", password)
            intent.putExtra("username", username)
            startActivity(intent)

        }
        BtnTemp.setOnClickListener() {
            val intent = Intent(this, TemperatureActivity::class.java)
            startActivity(intent)

        }
        BtnHum.setOnClickListener() {
            val intent = Intent(this, HumidityActivity::class.java)
            startActivity(intent)

        }
        Logout.setOnClickListener() {
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)

        }
        ImageBack.setOnClickListener() {
            val intent2 = Intent(this, HivesActivity::class.java)
            if (username != null && password != null ) {
                ApiCall().gethives(this, username, password) { payload ->


                    val hivesString = payload.hives

                    val hivesList = hivesString.split(",")

                    val intent = Intent(this, HivesActivity::class.java)

                    intent.putStringArrayListExtra("hivesData", ArrayList(hivesList))
                    intent.putExtra("password", password)
                    intent.putExtra("username", username)

                    startActivity(intent)


                }
            }
            startActivity(intent2)
        }
        BtnLight.setOnClickListener() {


            ImageLight.setImageResource(R.drawable.lighton)

            if (hiveData != null && username != null && password != null) {
                ApiCall().getsensor(this, hiveData, username, password) { payload ->
                    var lig = payload.lights
                    var str =""

                    if (lig == true)
                        str = "${baseUrl}/"+hiveData+"/lights?value=false"
                    else
                        str = "${baseUrl}/"+hiveData+"/lights?value=true"
                    lig= !lig

                    val jsonParams = JSONObject()

                    val request = object : JsonObjectRequest(
                        Method.POST, str, jsonParams,
                        { response ->
                            // Handle response
                            if (lig == true) {
                                ValLight.text = "ON"
                                ImageLight.setImageResource(R.drawable.lighton)
                            } else {
                                ValLight.text = "OFF"
                                ImageLight.setImageResource(R.drawable.light)
                            }
                        },
                        { error ->
                            // Handle error
                            Log.e("MainActivity", "Error during API call: ${error.localizedMessage}")
                        }) {

                        @Throws(AuthFailureError::class)
                        override fun getHeaders(): Map<String, String> {
                            val headers = HashMap<String, String>()
                            // Add your Authorization token here
                            val credentials = username+ ":" +password // Replace with your credentials
                            val auth = "Basic " + Base64.encodeToString(credentials.toByteArray(), Base64.NO_WRAP)
                            headers["Authorization"] = auth
                            return headers
                        }
                    }

// Add the request to the request queue
                    Volley.newRequestQueue(this).add(request)
                }
            }
        }
        BtnHeat.setOnClickListener() {


            if (hiveData != null && username != null && password != null) {
                ApiCall().getsensor(this, hiveData, username, password) { payload ->
                    var heat = payload.heating
                    var str =""

                    if (heat == true)
                        str = "${baseUrl}/"+hiveData+"/heating?value=false"
                    else
                        str = "${baseUrl}/"+hiveData+"/heating?value=true"

                    heat= !heat!!

                    val jsonParams = JSONObject()

                    val request = object : JsonObjectRequest(
                        Method.POST, str, jsonParams,
                        { response ->

                            if (heat == true) {
                                ValHeat.text = "ON"
                                ImageHeat.setImageResource(R.drawable.heatingon)
                            } else{
                                ValHeat.text = "OFF"
                                ImageHeat.setImageResource(R.drawable.heating)
                            }

                        },
                        { error ->
                            Log.e("MainActivity", "Error during API call: ${error.localizedMessage}")

                        }){

                        @Throws(AuthFailureError::class)
                        override fun getHeaders(): Map<String, String> {
                            val headers = HashMap<String, String>()
                            // Add your Authorization token here
                            val credentials = username+ ":" +password // Replace with your credentials
                            val auth = "Basic " + Base64.encodeToString(credentials.toByteArray(), Base64.NO_WRAP)
                            headers["Authorization"] = auth
                            return headers
                        }

                    }
                    Volley.newRequestQueue(this).add(request)
                }
            }
        }
    }

}


 fun getHeaders(): Map<String, String> {
    val headers = HashMap<String, String>()
    // Add your Authorization token here
    val credentials = "username:password" // Replace with your credentials
    val auth = "Basic " + Base64.encodeToString(credentials.toByteArray(), Base64.NO_WRAP)
    headers["Authorization"] = auth
    return headers
}