use bsky_sdk::BskyAgent;
use crate::clean::clean_content;
use atrium_api::types::string::Did;
use markov::Chain;
use anyhow::{Result, anyhow};
use tracing::{info, debug};

pub async fn retrieve_posts(agent: &BskyAgent, did: Did) -> Result<Vec<String>> {
    let mut post_list = Vec::new();
    let mut cursor = None;

    info!("Starting to retrieve posts for client ID: {}", did.as_str());

    loop {
        let output = agent.api.com.atproto.repo.list_records(
            atrium_api::com::atproto::repo::list_records::ParametersData {
                collection: "app.bsky.feed.post".parse().map_err(|e| anyhow!("{:?}", e))?,
                repo: did.as_str().parse().map_err(|e| anyhow!("{:?}", e))?,
                cursor: cursor.clone(),
                limit: Some(100.try_into().map_err(|e| anyhow!("{:?}", e))?),
                reverse: None,
            }.into()
        ).await?;

        let data = output.data;
        let records_len = data.records.len();
        for record in &data.records {
            if let Ok(post_record) = serde_json::from_value::<atrium_api::app::bsky::feed::post::Record>(serde_json::to_value(&record.value)?) {
                post_list.push(clean_content(&post_record.text));
            }
        }

        info!("Retrieved {} posts.", records_len);
        
        cursor = data.cursor;
        if cursor.is_none() {
            break;
        }
    }

    info!("Completed retrieval of posts for client ID: {}. Total posts retrieved: {}", did.as_str(), post_list.len());
    Ok(post_list)
}

pub fn refresh_dataset(source_posts: Vec<String>) -> Chain<String> {
    let mut chain = Chain::new();
    for post in source_posts {
        chain.feed_str(&post);
    }
    info!("Markov dataset refreshed.");
    chain
}

pub fn generate_text(chain: &Chain<String>, char_limit: usize) -> String {
    let generated = chain.generate_str();
    if generated.is_empty() {
        return String::new();
    }
    
    let mut result = generated;
    if result.len() > char_limit {
        result.truncate(char_limit);
    }
    debug!("Generated Text: {}", result);
    result
}
