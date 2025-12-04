public class Movement_Tags
{
    // `movement_id` BIGINT UNSIGNED NOT NULL,
    //     `tag_id` BIGINT UNSIGNED NOT NULL,
    //     PRIMARY KEY (`movement_id`,`tag_id`),
    // CONSTRAINT fk_movtag_mov FOREIGN KEY (`movement_id`) REFERENCES `movements`(`id`),
    // CONSTRAINT fk_movtag_tag FOREIGN KEY (`tag_id`) REFERENCES `tag`(`id`)
}
