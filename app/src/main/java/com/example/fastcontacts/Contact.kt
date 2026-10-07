package com.example.fastcontacts

data class Phone(val number: String, val type: String)
data class Email(val address: String, val type: String)

data class Contact(
    val id: Long,
    val name: String,
    val firstName: String,
    val lastName: String,
    val phones: List<Phone> = emptyList(),
    val emails: List<Email> = emptyList(),
    val starred: Boolean = false,
    val lookupKey: String = ""
)
