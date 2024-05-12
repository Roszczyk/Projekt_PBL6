package com.example.hive

import android.content.Context
import android.util.Log
import android.widget.Toast
import com.google.gson.GsonBuilder
import okhttp3.Credentials
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class BasicAuthInterceptor(username: String, password: String) : Interceptor {
    private var credentials: String = Credentials.basic(username, password)

    override fun intercept(chain: Interceptor.Chain): okhttp3.Response {
        var request = chain.request()
        request = request.newBuilder().header("Authorization", credentials).build()
        return chain.proceed(request)
    }
}

class ApiCall {

    fun getsensor(context: Context, callback: (DataModel) -> Unit) {

        val client = OkHttpClient.Builder()
            .addInterceptor(BasicAuthInterceptor("admin", "admin"))
            .build()

        val gson = GsonBuilder()
            .setLenient()
            .create()

        val retrofit: Retrofit = Retrofit.Builder()
            .baseUrl("http://10.0.2.2:5000/")
            .client(client) // Set the custom OkHttpClient
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()

        val service: ApiService = retrofit.create(ApiService::class.java)

        val call: Call<DataModel> = service.getsensors()

        call.enqueue(object : Callback<DataModel> {

            override fun onResponse(call: Call<DataModel>, response: Response<DataModel>) {
                // This method is called when the API response is received successfully.
                if (response.isSuccessful) {
                    val telemetry: DataModel? = response.body()
                    telemetry?.let { callback(it) }
                }
            }

            override fun onFailure(call: Call<DataModel>, t: Throwable) {
                // This method is called when the API request fails.
                Toast.makeText(context, "Request Fail", Toast.LENGTH_SHORT).show()
            }
        })
    }

    fun gethives(context: Context, username: String, password: String, callback: (DataHives) -> Unit) {

        val client = OkHttpClient.Builder()
            .addInterceptor(BasicAuthInterceptor(username,password))
            .build()

        val gson = GsonBuilder()
            .setLenient()
            .create()

        val retrofit: Retrofit = Retrofit.Builder()
            .baseUrl("http://10.0.2.2:5000/")
            .client(client) // Set the custom OkHttpClient
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()

        val service: ApiService = retrofit.create(ApiService::class.java)

        val call: Call<DataHives> = service.gethives(username)

        call.enqueue(object : Callback<DataHives> {

            override fun onResponse(call: Call<DataHives>, response: Response<DataHives>) {

                if (response.isSuccessful) {
                    val telemetry: DataHives? = response.body()
                    telemetry?.let { callback(it) }
                }
                else{
                    Toast.makeText(context,"Login failed. Please check your credentials.",Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<DataHives>, t: Throwable) {
                // This method is called when the API request fails.
                Toast.makeText(context,"Login failed. Please check your credentials.",Toast.LENGTH_SHORT).show()

            }
        })

    }
}
