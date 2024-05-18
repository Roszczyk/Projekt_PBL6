package com.example.hive

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import org.java_websocket.client.WebSocketClient
import org.java_websocket.handshake.ServerHandshake
import android.app.NotificationChannel
import android.app.NotificationManager
import androidx.core.app.NotificationCompat
import java.net.URI
import android.app.PendingIntent
import android.content.Context
import android.os.Build
import androidx.annotation.RequiresApi
import java.util.*
import java.nio.charset.StandardCharsets
import java.util.Base64



class HivesActivity : AppCompatActivity() {

    private var text: TextView? = null
    lateinit var webSocketClient: WebSocketClient
    private val channelId = "WebSocketChannel"
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        createNotificationChannel()
        setContentView(R.layout.hives_activity)
        val uri = URI("ws://10.0.2.2:8765") // Adres IP serwera
//        // Tworzenie nagłówka autoryzacji Basic
//        val auth = Base64.encodeToString("user:password".toByteArray(), Base64.NO_WRAP)
//        val headers = HashMap<String, String>()
//        headers["Authorization"] = "Basic $auth"
        val authHeader = "Basic " + Base64.getEncoder().encodeToString("user:password".toByteArray(StandardCharsets.UTF_8))

        webSocketClient = object : WebSocketClient(uri, mapOf("Authorization" to authHeader)) {
            override fun onOpen(handshakedata: ServerHandshake?) {
                // Połączenie nawiązane
                Log.d("SCANNER","WebSocket connected")
            }

            override fun onMessage(message: String?) {
                // Odebrano wiadomość
                runOnUiThread {
                    Log.d("SCANNER","Received: $message")
                    println("Received: $message")
                    showNotification(message)
                }
            }

            override fun onClose(code: Int, reason: String?, remote: Boolean) {
                // Połączenie zamknięte
                Log.d("SCANNER","WebSocket connection closed")
            }

            override fun onError(ex: Exception?) {
                // Błąd połączenia
                Log.d("SCANNER","Error: ${ex?.message}")
            }
        }

        webSocketClient.connect()

        val hivesList = intent.getStringArrayListExtra("hivesData")
        val password = intent.getStringExtra("password")
        val username = intent.getStringExtra("username")

        val spinner: Spinner = findViewById(R.id.hivesSpinner)

        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, hivesList.orEmpty())

        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

        spinner.adapter = adapter

        var selectedHive: String? = null

        spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                selectedHive = parent?.getItemAtPosition(position) as String
                Log.d("HivesActivity", "Selected hive: $selectedHive")
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {

            }
        }

        val button: Button = findViewById(R.id.button)

        button.setOnClickListener {

            if (selectedHive != null) {
                val intent = Intent(this, MainActivity::class.java)
                intent.putExtra("selectedHive", selectedHive!!)
                intent.putExtra("password", password)
                intent.putExtra("username", username)
                startActivity(intent)
            } else {
                Toast.makeText(this, "Please select a hive", Toast.LENGTH_SHORT).show()
            }
        }



    }
    override fun onDestroy() {
        super.onDestroy()
        webSocketClient.close()
    }
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = getString(R.string.channel_name)
            val descriptionText = getString(R.string.channel_description)
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(channelId, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun showNotification(message: String?) {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)

        val builder = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.drawable.icon)
            .setContentTitle("Nowe powiadomienie")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_CALL)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)

        val notificationManager: NotificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        notificationManager.notify(0, builder.build())
    }
}


