package com.example.fastcontacts

import android.content.Context
import android.provider.ContactsContract

object ContactsRepository {

    fun loadAll(context: Context): List<Contact> = load(context, null)

    fun loadById(context: Context, id: Long): Contact? = load(context, id).firstOrNull()

    private fun load(context: Context, onlyId: Long?): List<Contact> {
        val contactsMap = LinkedHashMap<Long, MutableContact>()
        val cr = context.contentResolver

        val cSel = if (onlyId != null) "${ContactsContract.Contacts._ID}=?" else null
        val cArgs = if (onlyId != null) arrayOf(onlyId.toString()) else null

        val cursor = cr.query(
            ContactsContract.Contacts.CONTENT_URI,
            arrayOf(
                ContactsContract.Contacts._ID,
                ContactsContract.Contacts.DISPLAY_NAME_PRIMARY,
                ContactsContract.Contacts.STARRED,
                ContactsContract.Contacts.LOOKUP_KEY
            ),
            cSel, cArgs, "${ContactsContract.Contacts.DISPLAY_NAME_PRIMARY} ASC"
        )

        cursor?.use {
            val idIdx = it.getColumnIndex(ContactsContract.Contacts._ID)
            val nameIdx = it.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME_PRIMARY)
            val starIdx = it.getColumnIndex(ContactsContract.Contacts.STARRED)
            val lookupIdx = it.getColumnIndex(ContactsContract.Contacts.LOOKUP_KEY)
            while (it.moveToNext()) {
                val id = it.getLong(idIdx)
                val name = it.getString(nameIdx) ?: "Unknown"
                val starred = it.getInt(starIdx) == 1
                val lookup = it.getString(lookupIdx) ?: ""
                contactsMap[id] = MutableContact(id, name, starred, lookup)
            }
        }

        if (contactsMap.isEmpty()) return emptyList()

        val nameMap = HashMap<Long, Pair<String, String>>()
        val nameSel = if (onlyId != null) {
            "${ContactsContract.Data.MIMETYPE}=? AND ${ContactsContract.Data.CONTACT_ID}=?"
        } else {
            "${ContactsContract.Data.MIMETYPE}=?"
        }
        val nameArgs = if (onlyId != null) {
            arrayOf(ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE, onlyId.toString())
        } else {
            arrayOf(ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE)
        }

        val nameCursor = cr.query(
            ContactsContract.Data.CONTENT_URI,
            arrayOf(
                ContactsContract.Data.CONTACT_ID,
                ContactsContract.CommonDataKinds.StructuredName.GIVEN_NAME,
                ContactsContract.CommonDataKinds.StructuredName.FAMILY_NAME
            ),
            nameSel, nameArgs, null
        )

        nameCursor?.use {
            val cIdIdx = it.getColumnIndex(ContactsContract.Data.CONTACT_ID)
            val givenIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.StructuredName.GIVEN_NAME)
            val familyIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.StructuredName.FAMILY_NAME)
            while (it.moveToNext()) {
                val cId = it.getLong(cIdIdx)
                val given = it.getString(givenIdx) ?: ""
                val family = it.getString(familyIdx) ?: ""
                if (!nameMap.containsKey(cId) || (given.isNotBlank() || family.isNotBlank())) {
                    nameMap[cId] = Pair(given, family)
                }
            }
        }

        nameMap.forEach { (cId, pair) ->
            contactsMap[cId]?.let {
                it.firstName = pair.first
                it.lastName = pair.second
            }
        }

        val pSel = if (onlyId != null) "${ContactsContract.CommonDataKinds.Phone.CONTACT_ID}=?" else null
        val phoneCursor = cr.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            arrayOf(
                ContactsContract.CommonDataKinds.Phone.CONTACT_ID,
                ContactsContract.CommonDataKinds.Phone.NUMBER,
                ContactsContract.CommonDataKinds.Phone.TYPE,
                ContactsContract.CommonDataKinds.Phone.LABEL
            ),
            pSel, cArgs, null
        )

        phoneCursor?.use {
            val cIdIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.CONTACT_ID)
            val numIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
            val typeIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.TYPE)
            val labelIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.LABEL)
            while (it.moveToNext()) {
                val cId = it.getLong(cIdIdx)
                val num = it.getString(numIdx) ?: continue
                val typeInt = it.getInt(typeIdx)
                val custom = it.getString(labelIdx) ?: ""
                val typeLabel = ContactsContract.CommonDataKinds.Phone.getTypeLabel(
                    context.resources, typeInt, custom
                ).toString()
                contactsMap[cId]?.addPhone(Phone(num, typeLabel))
            }
        }

        val eSel = if (onlyId != null) "${ContactsContract.CommonDataKinds.Email.CONTACT_ID}=?" else null
        val emailCursor = cr.query(
            ContactsContract.CommonDataKinds.Email.CONTENT_URI,
            arrayOf(
                ContactsContract.CommonDataKinds.Email.CONTACT_ID,
                ContactsContract.CommonDataKinds.Email.ADDRESS,
                ContactsContract.CommonDataKinds.Email.TYPE,
                ContactsContract.CommonDataKinds.Email.LABEL
            ),
            eSel, cArgs, null
        )

        emailCursor?.use {
            val cIdIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.CONTACT_ID)
            val addrIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.ADDRESS)
            val typeIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.TYPE)
            val labelIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Email.LABEL)
            while (it.moveToNext()) {
                val cId = it.getLong(cIdIdx)
                val addr = it.getString(addrIdx) ?: continue
                val typeInt = it.getInt(typeIdx)
                val custom = it.getString(labelIdx) ?: ""
                val typeLabel = ContactsContract.CommonDataKinds.Email.getTypeLabel(
                    context.resources, typeInt, custom
                ).toString()
                contactsMap[cId]?.addEmail(Email(addr, typeLabel))
            }
        }

        return contactsMap.values.map { it.toContact() }
    }

    private class MutableContact(
        val id: Long,
        val name: String,
        val starred: Boolean,
        val lookupKey: String
    ) {
        var firstName: String = ""
        var lastName: String = ""
        val phones = mutableListOf<Phone>()
        val emails = mutableListOf<Email>()

        fun addPhone(p: Phone) {
            val digits = p.number.filter { it.isDigit() }
            if (phones.none { it.number.filter { c -> c.isDigit() } == digits }) {
                phones.add(p)
            }
        }

        fun addEmail(e: Email) {
            if (emails.none { it.address.equals(e.address, ignoreCase = true) }) {
                emails.add(e)
            }
        }

        fun toContact(): Contact {
            val effFirst = firstName.ifBlank { name.trim().split(" ").firstOrNull() ?: "" }
            val effLast = lastName.ifBlank {
                val parts = name.trim().split(" ")
                if (parts.size > 1) parts.last() else ""
            }
            return Contact(id, name, effFirst, effLast, phones, emails, starred, lookupKey)
        }
    }
}
