package com.example.hive

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import org.java_websocket.client.WebSocketClient
import org.java_websocket.handshake.ServerHandshake
import org.json.JSONObject
import java.net.URI
import java.nio.charset.StandardCharsets
import java.util.Base64

object WebSocketManager {
    private var webSocketClient: WebSocketClient? = null
    private const val uri = "ws://10.0.2.2:8765"
    var messageListener: ((String) -> Unit)? = null

    fun getWebSocketClient(username: String, password: String, context: Context, channelId: String): WebSocketClient {
        if (webSocketClient == null) {
            val authHeader = "Basic " + Base64.getEncoder().encodeToString("$username:$password".toByteArray(StandardCharsets.UTF_8))
            webSocketClient = object : WebSocketClient(URI(uri), mapOf("Authorization" to authHeader)) {
                override fun onOpen(handshakedata: ServerHandshake?) {
                    Log.d("WebSocketManager", "WebSocket connected")
                }

                override fun onMessage(message: String?) {
                    Log.d("WebSocketManager", "Received: $message")
                    message?.let {
                        try {
                            // Parse the JSON string
                            val jsonObject = JSONObject(it)
                            // Extract the message value
                            val parsedMessage = jsonObject.getString("message")

                            // Invoke the message listener with the parsed message
                            messageListener?.invoke(parsedMessage)

                            // Show the notification with the parsed message
                            showNotification(context, channelId, parsedMessage)
                        } catch (e: Exception) {
                            Log.e("WebSocketManager", "Failed to parse message: $it", e)
                        }
                    }
                }


                override fun onClose(code: Int, reason: String?, remote: Boolean) {
                    Log.d("WebSocketManager", "WebSocket connection closed")
                }

                override fun onError(ex: Exception?) {
                    Log.d("WebSocketManager", "Error: ${ex?.message}")
                }
            }
            webSocketClient!!.connect()
        }
        return webSocketClient!!
    }

    fun closeWebSocket() {
        webSocketClient?.close()
        webSocketClient = null
    }

    fun createNotificationChannel(context: Context, channelId: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "WebSocket Notifications"
            val descriptionText = "Channel for WebSocket notifications"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(channelId, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    private fun showNotification(context: Context, channelId: String, message: String) {
        val intent = Intent(context, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.icon)
            .setContentTitle("Nowe powiadomienie")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_MESSAGE)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)

        with(NotificationManagerCompat.from(context)) {
            notify(0, builder.build())
        }
    }


}
