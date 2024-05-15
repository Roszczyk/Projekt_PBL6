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

class HivesActivity : AppCompatActivity() {

    private var text: TextView? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.hives_activity)

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



}