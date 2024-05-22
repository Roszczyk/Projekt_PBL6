// HivesActivity.kt
package com.example.hive

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.Spinner
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.annotation.RequiresApi
import android.os.Build
import android.app.NotificationChannel
import android.app.NotificationManager
import androidx.core.app.NotificationCompat
import android.app.PendingIntent
import android.content.Context
import com.example.hive.WebSocketManager.createNotificationChannel

class HivesActivity : AppCompatActivity() {

    private val channelId = "WebSocketChannel"
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WebSocketManager.createNotificationChannel(this, channelId)
        setContentView(R.layout.hives_activity)

        val username = intent.getStringExtra("username") ?: ""
        val password = intent.getStringExtra("password") ?: ""

        // Pobierz WebSocketClient z singletona
        val webSocketClient = WebSocketManager.getWebSocketClient(username, password, this, channelId)

        // Ustaw listener dla wiadomości z WebSocket
        WebSocketManager.messageListener = { message ->
            runOnUiThread {
                Log.d("HivesActivity", "Received: $message")

            }
        }

        val hivesList = intent.getStringArrayListExtra("hivesData")

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

            override fun onNothingSelected(parent: AdapterView<*>?) {}
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
        WebSocketManager.closeWebSocket()
    }

//    private fun createNotificationChannel() {
//        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
//            val name = getString(R.string.channel_name)
//            val descriptionText = getString(R.string.channel_description)
//            val importance = NotificationManager.IMPORTANCE_DEFAULT
//            val channel = NotificationChannel(channelId, name, importance).apply {
//                description = descriptionText
//            }
//            val notificationManager: NotificationManager =
//                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
//            notificationManager.createNotificationChannel(channel)
//        }
//    }
//
//    private fun showNotification(message: String?) {
//        val intent = Intent(this, MainActivity::class.java)
//        val pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
//
//        val builder = NotificationCompat.Builder(this, channelId)
//            .setSmallIcon(R.drawable.icon)
//            .setContentTitle("Nowe powiadomienie")
//            .setContentText(message)
//            .setPriority(NotificationCompat.PRIORITY_HIGH)
//            .setCategory(NotificationCompat.CATEGORY_CALL)
//            .setContentIntent(pendingIntent)
//            .setAutoCancel(true)
//
//        val notificationManager: NotificationManager =
//            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
//
//        notificationManager.notify(0, builder.build())
//    }
}
