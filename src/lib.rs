extern crate leptess;
use pyo3::prelude::*; 

// use std::any::type_name;
use chat_gpt_lib_rs::{ChatGPTClient, ChatInput, Message, Model, Role};
use leptess::{leptonica, tesseract};
use std::path::Path;

// use std::borrow::Borrow;

// variable type checker
// fn type_of<T>(_: T) -> &'static str {
//     type_name::<T>()
// }

#[tokio::main]
#[pyfunction]
async fn chatgpt(text: String, api_key: String) -> String {
    let base_url = "https://api.openai.com";
    let client = ChatGPTClient::new(&api_key, base_url);

    let chat_input = ChatInput {
        model: Model::Gpt3_5Turbo,
        messages: vec![
            Message {
                role: Role::System,
                content: "You are a helpful assistant.".to_string(),
            },
            Message {
                role: Role::User,
                content: ("Show possible allergy infos and health benefits of the following ingredients: ".to_owned() + &text).to_string(),
            },
        ],
        ..Default::default()
    };

    let response = client.chat(chat_input).await.unwrap();
    let result =  &response.choices[0].message.content;

    return result.to_string()

}

#[pyfunction]
fn text_recognition(img_path: String) -> String {
    let mut api = tesseract::TessApi::new(None, "eng").unwrap();

    let pix = leptonica::pix_read(Path::new(&img_path)).unwrap();
    api.set_image(&pix);

    if api.get_source_y_resolution() <= 0 {
        api.set_image(&pix);
    }

    let text = api.get_utf8_text();
    return text.unwrap().to_string();

//  println!({}, type_of(text.wrap()))
}

#[pymodule]
fn food_scanner(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(text_recognition,m)?)?;
    m.add_function(wrap_pyfunction!(chatgpt,m)?)?;
    Ok(())
}
