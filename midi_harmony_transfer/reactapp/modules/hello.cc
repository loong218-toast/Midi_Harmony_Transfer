#include <node.h>

namespace hello_module {
  using v8::FunctionCallbackInfo;
  using v8::Isolate;
  using v8::Local;
  using v8::Object;
  using v8::String;
  using v8::Value;
  
  void sayHello(const FunctionCallbackInfo<Value>& args) {
    Isolate* isolate = args.GetIsolate();
    args.GetReturnValue().Set(String::NewFromUtf8(isolate, "Hello World!"));
  }
  
  // the initialization function for hello_module
  void init(Local<Object> exports) {
    NODE_SET_METHOD(exports, "sayHello", sayHello);
  }
  
  // node.h C++ macro to export the initialization function
  // (macros should not end by semicolon)
  NODE_MODULE(NODE_GYP_MODULE_NAME, init)
}