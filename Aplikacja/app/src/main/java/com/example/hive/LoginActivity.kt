package com.example.hive

import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class LoginActivity : AppCompatActivity() {
    private var usernameEditText: EditText? = null
    private var passwordEditText: EditText? = null
    private var loginButton: Button? = null
    private var test: TextView? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.login_activity)

        // Inicjalizacja elementów interfejsu użytkownika
        val imageView = findViewById<ImageView>(R.id.imageView)
        usernameEditText = findViewById<EditText>(R.id.username)
        passwordEditText = findViewById<EditText>(R.id.password)
        loginButton = findViewById<Button>(R.id.button)

        // Obsługa logowania po kliknięciu przycisku
        loginButton?.setOnClickListener() {
            loginUser()
        }
    }

    // Metoda do obsługi logowania
    private fun loginUser() {
        val username = usernameEditText!!.getText().toString().trim { it <= ' ' }
        val password = passwordEditText!!.getText().toString().trim { it <= ' ' }

        // Tutaj możesz dodać logikę logowania, np. wysłanie żądania do serwera
        // i przetworzenie odpowiedzi, aby sprawdzić poprawność danych logowania

        // Przykładowa logika - sprawdzenie, czy pola są puste
        if (username.isEmpty()) {
            usernameEditText!!.error = "Username is required"
            usernameEditText!!.requestFocus()
            return
        }
        if (password.isEmpty()) {
            passwordEditText!!.error = "Password is required"
            passwordEditText!!.requestFocus()
            return
        }

        ApiCall().gethives(this, username, password) { payload ->


            Log.d("SCANER", "${payload.hives}")
            Log.d("SCANER", "cokolwiek")


        }

    }
}
