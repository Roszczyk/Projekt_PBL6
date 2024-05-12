package com.example.hive

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Path

interface ApiService {

    @GET("{device}/sensors")
    fun getsensors(@Path("device") device: String): Call<DataModel>

    @GET("/{user}/hives")
    fun gethives(@Path("user") user: String): Call<DataHives>
}
