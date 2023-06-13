#include <stdio.h>
#include <stdlib.h>
#include <dbus/dbus.h>

int main(int argc, char** argv) {
    DBusConnection* conn;
    DBusError err;
    DBusMessage* msg;
    DBusMessageIter args;
    DBusPendingCall* pending;
    int ret;
    char* reply;

    // 1. 初始化DBus库和错误结构体
    dbus_error_init(&err);
    conn = dbus_bus_get(DBUS_BUS_SESSION, &err);

    if (dbus_error_is_set(&err)) {
        fprintf(stderr, "Connection Error (%s)\n", err.message);
        dbus_error_free(&err);
        return EXIT_FAILURE;
    }

    // 2. 创建DBus消息
    msg = dbus_message_new_method_call("org.freedesktop.DBus",    // Bus name
                                       "/",                      // Object path
                                       "org.freedesktop.DBus",    // Interface name
                                       "ListNames");             // Method name

    if (msg == NULL) {
        fprintf(stderr, "Message Null\n");
        return EXIT_FAILURE;
    }

    // 3. 发送DBus消息
    ret = dbus_connection_send_with_reply(conn, msg, &pending, -1);

    if (ret == DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER) {
        dbus_connection_flush(conn);

        if (dbus_pending_call_set_notify(pending, NULL, NULL, NULL) == FALSE) {
            fprintf(stderr, "Out of Memory\n");
            return EXIT_FAILURE;
        }

        // 4. 等待DBus Daemon的回复
        dbus_pending_call_block(pending);

        // 5. 解析DBus Daemon的回复
        msg = dbus_pending_call_steal_reply(pending);
        if (msg == NULL) {
            fprintf(stderr, "Reply Null\n");
            return EXIT_FAILURE;
        }

        dbus_message_iter_init(msg, &args);
        if (dbus_message_iter_get_arg_type(&args) != DBUS_TYPE_ARRAY) {
            fprintf(stderr, "Invalid Reply\n");
            return EXIT_FAILURE;
        }

        dbus_message_iter_get_basic(&args, &reply);
        printf("Reply: %s\n", reply);

        dbus_message_unref(msg);
    } else {
        fprintf(stderr, "Error: %d\n", ret);
        return EXIT_FAILURE;
    }

    dbus_connection_close(conn);
    return EXIT_SUCCESS;
}