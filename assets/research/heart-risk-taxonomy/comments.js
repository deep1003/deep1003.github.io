import { commentsConfig } from './comments-config.js';
import { createCommentsApi } from './comments-api.js';
import { mountComments } from './comments-ui.js';

if (commentsConfig.enabled && commentsConfig.url) {
  mountComments(createCommentsApi(commentsConfig.url));
}
