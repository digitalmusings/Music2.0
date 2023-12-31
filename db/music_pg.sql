CREATE TABLE "submission" (
  "submission_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "participant_id" uuid NOT NULL,
  "bracket_id" uuid NOT NULL,
  "song_id" uuid NOT NULL,
  "order" integer NOT NULL,
  "date_submitted" timestamp NOT NULL DEFAULT (now()),
  "active" bool NOT NULL,
  "is_dupe" bool NOT NULL,
  "title" text NOT NULL,
  "version" text,
  "artist" text,
  "collaborators" text,
  "composer" text,
  "link" text NOT NULL,
  "genre" text,
  "emoji" text,
  "comments" text
);

CREATE TABLE "submission_history" (
  "submission_history_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "update_date" timestamp NOT NULL,
  "update_note" text NOT NULL,
  "submission_id" uuid NOT NULL,
  "participant_id" uuid NOT NULL,
  "bracket_id" uuid NOT NULL,
  "song_id" uuid NOT NULL,
  "order" integer NOT NULL,
  "date_submitted" timestamp NOT NULL DEFAULT (now()),
  "active" bool NOT NULL,
  "is_dupe" bool NOT NULL,
  "title" text NOT NULL,
  "version" text,
  "artist" text,
  "collaborators" text,
  "composer" text,
  "link" text NOT NULL,
  "genre" text,
  "emoji" text,
  "comments" text
);

CREATE TABLE "link_relation" (
  "link_relation_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "parent_link_id" uuid NOT NULL,
  "child_link_id" uuid NOT NULL,
  "link_relation_type" text NOT NULL
);

CREATE TABLE "link" (
  "link_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "url" text NOT NULL,
  "region" text[]
);

CREATE TABLE "song" (
  "song_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "title" text NOT NULL,
  "title_english" text,
  "version" text,
  "artist" text NOT NULL,
  "collaborator" text,
  "composer" text,
  "year" integer,
  "year_alt" integer
);

CREATE TABLE "song_relation" (
  "song_relation_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "parent_song_id" uuid NOT NULL,
  "child_song_id" uuid NOT NULL,
  "song_relation_type" text NOT NULL
);

CREATE TABLE "song_artist" (
  "song_artist_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "song_id" uuid NOT NULL,
  "artist_id" uuid NOT NULL,
  "credit_type" text NOT NULL
);

CREATE TABLE "artist" (
  "artist_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "name" text NOT NULL,
  "year_min" integer,
  "year_max" integer,
  "primary_artist_id" uuid
);

CREATE TABLE "artist_genre" (
  "artist_genre_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "artist_id" uuid NOT NULL,
  "genre_id" uuid NOT NULL
);

CREATE TABLE "participant" (
  "participant_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "username" text NOT NULL,
  "discriminator" integer NULL,
  "nickname" text,
  "date_joined" timestamp NOT NULL DEFAULT (now()),
  "time_zone" text,
  "active" bool NOT NULL
);

CREATE TABLE "participant_nickname" (
  "participant_nickname_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "participant_id" uuid NOT NULL,
  "nickname" text NOT NULL,
  "date_start" date NOT NULL,
  "date_end" date
);

CREATE TABLE "genre" (
  "genre_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "name" text UNIQUE NOT NULL,
  "parent_id" text
);

CREATE TABLE "genre_relation" (
  "genre_relation_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "parent_genre_id" uuid NOT NULL,
  "child_genre_id" uuid NOT NULL
);

CREATE TABLE "song_genre" (
  "song_genre_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "song_id" uuid NOT NULL,
  "genre_id" uuid NOT NULL
);

CREATE TABLE "bracket" (
  "bracket_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "epoch" integer,
  "cycle" integer,
  "name" text,
  "type" text NOT NULL,
  "year_min" integer,
  "year_max" integer,
  "order" integer NOT NULL,
  "size" integer NOT NULL,
  "date_start" timestamp,
  "date_end" timestamp,
  "discord_message_id" text
);

CREATE TABLE "project" (
  "project_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "name" text UNIQUE,
  "project_lead_id" uuid
);

CREATE TABLE "bracket_selection" (
  "bracket_selection_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "project_id" uuid NOT NULL,
  "epoch" integer NOT NULL,
  "cycle" integer NOT NULL,
  "bracket_id" uuid NOT NULL,
  "date_selected" timestamp NOT NULL
);

CREATE TABLE "seed" (
  "seed_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "bracket_id" uuid NOT NULL,
  "seed" integer NOT NULL,
  "submission_id" uuid NOT NULL,
  "emoji" text
);

CREATE TABLE "seed_history" (
  "seed_history_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "date_changed" timestamp NOT NULL,
  "reason_changed" text NOT NULL,
  "seed_id" uuid NOT NULL,
  "submission_id" uuid NOT NULL,
  "emoji" text
);

CREATE TABLE "round" (
  "round_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "bracket_id" uuid NOT NULL,
  "name" text NOT NULL,
  "size" integer NOT NULL,
  "index_asc" integer NOT NULL,
  "index_desc" integer NOT NULL,
  "date_start" timestamp NOT NULL,
  "date_end" timestamp,
  "discord_message_id" text
);

CREATE TABLE "match" (
  "match_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "round_id" uuid NOT NULL,
  "index" integer NOT NULL,
  "date_posted" timestamp NOT NULL,
  "tie" text,
  "winner_id" uuid,
  "date_cancelled" timestamp,
  "reason_cancelled" text,
  "next_match_id" uuid,
  "discord_message_id" text
);

CREATE TABLE "match_seed" (
  "match_seed_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "match_id" uuid NOT NULL,
  "seed_id" uuid NOT NULL,
  "index" integer NOT NULL,
  "votes" integer,
  "voters" text[] NOT NULL,
  "previous_match_id" uuid
);

CREATE TABLE "notification" (
  "notification_id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "participant_id" uuid NOT NULL,
  "submission_id" uuid,
  "date_first_attempt" timestamp NOT NULL,
  "date_succeded" timestamp,
  "notification_type" text NOT NULL,
  "discord_message_id" text
);

CREATE TABLE "config" (
  "project_id" uuid NOT NULL,
  "key" text,
  "value" text,
  PRIMARY KEY ("project_id", "key")
);


CREATE INDEX ON "submission_history" ("submission_id");

CREATE INDEX ON "submission_history" ("participant_id");

CREATE INDEX ON "submission_history" ("bracket_id");

CREATE INDEX ON "submission_history" ("song_id");

CREATE INDEX ON "link_relation" ("parent_link_id");

CREATE INDEX ON "link_relation" ("child_link_id");

CREATE INDEX ON "song_relation" ("parent_song_id");

CREATE INDEX ON "song_relation" ("child_song_id");

CREATE UNIQUE INDEX ON "song_artist" ("song_id", "artist_id");

CREATE INDEX ON "participant_nickname" ("participant_id");

CREATE INDEX ON "genre" ("parent_id");

CREATE INDEX ON "genre_relation" ("parent_genre_id");

CREATE INDEX ON "genre_relation" ("child_genre_id");

CREATE UNIQUE INDEX ON "song_genre" ("song_id", "genre_id");

CREATE UNIQUE INDEX ON "seed" ("bracket_id", "seed");

CREATE INDEX ON "seed" ("submission_id");

CREATE INDEX ON "seed_history" ("seed_id");

CREATE INDEX ON "seed_history" ("submission_id");

CREATE INDEX ON "round" ("bracket_id");

CREATE INDEX ON "match" ("round_id");

COMMENT ON COLUMN "submission_history"."update_note" IS 'dupe ineligible withdrawn "play-in loser"';

COMMENT ON COLUMN "link_relation"."link_relation_type" IS 'submission song seed';

COMMENT ON COLUMN "link"."region" IS 'US Canada Japan Australia Europe Asia "North America" "South America" Africa Worldwide';

COMMENT ON COLUMN "song"."artist" IS 'CALCULATED';

COMMENT ON COLUMN "song"."collaborator" IS 'CALCULATED';

COMMENT ON COLUMN "song_relation"."song_relation_type" IS 'cover live';

COMMENT ON COLUMN "song_artist"."credit_type" IS 'primary collaborator original remixer composer';

COMMENT ON COLUMN "participant"."nickname" IS 'CALCULATED';

COMMENT ON COLUMN "bracket"."type" IS 'year theme aggregate';

COMMENT ON COLUMN "bracket"."size" IS '128 96 64 48 32';

COMMENT ON COLUMN "seed_history"."reason_changed" IS '"missed dupe" ineligible';

COMMENT ON COLUMN "round"."name" IS 'Finals "Third Place" "Semi-Finals" "Quarter-Finals" "Round of 16" "Round of 32" "Round of 64" "Round of 128" "Play-Ins"';

COMMENT ON COLUMN "round"."size" IS '0 means play-in round';

COMMENT ON COLUMN "round"."index_asc" IS '-1-indexed from Play-Ins';

COMMENT ON COLUMN "round"."index_desc" IS '0-indexed from finals';

COMMENT ON COLUMN "match"."tie" IS '0 (no), 1 (broken), 2 (kept)';

COMMENT ON COLUMN "match"."reason_cancelled" IS '"ineligible sub0" "ineligible sub1" "administrative error"';

COMMENT ON COLUMN "notification"."notification_type" IS '"need replacement" "no replacement" "tie"';

ALTER TABLE "submission" ADD FOREIGN KEY ("participant_id") REFERENCES "participant" ("participant_id");

ALTER TABLE "submission" ADD FOREIGN KEY ("bracket_id") REFERENCES "bracket" ("bracket_id");

ALTER TABLE "submission" ADD FOREIGN KEY ("song_id") REFERENCES "song" ("song_id");

ALTER TABLE "submission_history" ADD FOREIGN KEY ("submission_id") REFERENCES "submission" ("submission_id");

ALTER TABLE "submission_history" ADD FOREIGN KEY ("participant_id") REFERENCES "participant" ("participant_id");

ALTER TABLE "submission_history" ADD FOREIGN KEY ("bracket_id") REFERENCES "bracket" ("bracket_id");

ALTER TABLE "submission_history" ADD FOREIGN KEY ("song_id") REFERENCES "song" ("song_id");

ALTER TABLE "link_relation" ADD FOREIGN KEY ("parent_link_id") REFERENCES "link" ("link_id");

ALTER TABLE "link_relation" ADD FOREIGN KEY ("child_link_id") REFERENCES "link" ("link_id");

ALTER TABLE "song_relation" ADD FOREIGN KEY ("parent_song_id") REFERENCES "song" ("song_id");

ALTER TABLE "song_relation" ADD FOREIGN KEY ("child_song_id") REFERENCES "song" ("song_id");

ALTER TABLE "song_artist" ADD FOREIGN KEY ("song_id") REFERENCES "song" ("song_id");

ALTER TABLE "song_artist" ADD FOREIGN KEY ("artist_id") REFERENCES "artist" ("artist_id");

ALTER TABLE "artist" ADD FOREIGN KEY ("primary_artist_id") REFERENCES "artist" ("artist_id");

ALTER TABLE "artist_genre" ADD FOREIGN KEY ("artist_id") REFERENCES "artist" ("artist_id");

ALTER TABLE "artist_genre" ADD FOREIGN KEY ("genre_id") REFERENCES "genre" ("genre_id");

ALTER TABLE "participant_nickname" ADD FOREIGN KEY ("participant_id") REFERENCES "participant" ("participant_id");

ALTER TABLE "genre_relation" ADD FOREIGN KEY ("parent_genre_id") REFERENCES "genre" ("genre_id");

ALTER TABLE "genre_relation" ADD FOREIGN KEY ("child_genre_id") REFERENCES "genre" ("genre_id");

ALTER TABLE "song_genre" ADD FOREIGN KEY ("song_id") REFERENCES "song" ("song_id");

ALTER TABLE "song_genre" ADD FOREIGN KEY ("genre_id") REFERENCES "genre" ("genre_id");

ALTER TABLE "project" ADD FOREIGN KEY ("project_lead_id") REFERENCES "participant" ("participant_id");

ALTER TABLE "bracket_selection" ADD FOREIGN KEY ("project_id") REFERENCES "project" ("project_id");

ALTER TABLE "bracket_selection" ADD FOREIGN KEY ("bracket_id") REFERENCES "bracket" ("bracket_id");

ALTER TABLE "seed" ADD FOREIGN KEY ("bracket_id") REFERENCES "bracket" ("bracket_id");

ALTER TABLE "seed" ADD FOREIGN KEY ("submission_id") REFERENCES "submission" ("submission_id");

ALTER TABLE "seed_history" ADD FOREIGN KEY ("seed_id") REFERENCES "seed" ("seed_id");

ALTER TABLE "seed_history" ADD FOREIGN KEY ("submission_id") REFERENCES "submission" ("submission_id");

ALTER TABLE "round" ADD FOREIGN KEY ("bracket_id") REFERENCES "bracket" ("bracket_id");

ALTER TABLE "match" ADD FOREIGN KEY ("round_id") REFERENCES "round" ("round_id");

ALTER TABLE "match" ADD FOREIGN KEY ("winner_id") REFERENCES "submission" ("submission_id");

ALTER TABLE "match" ADD FOREIGN KEY ("next_match_id") REFERENCES "match" ("match_id");

ALTER TABLE "match_seed" ADD FOREIGN KEY ("match_id") REFERENCES "match" ("match_id");

ALTER TABLE "match_seed" ADD FOREIGN KEY ("seed_id") REFERENCES "seed" ("seed_id");

ALTER TABLE "match_seed" ADD FOREIGN KEY ("previous_match_id") REFERENCES "match" ("match_id");

ALTER TABLE "notification" ADD FOREIGN KEY ("participant_id") REFERENCES "participant" ("participant_id");

ALTER TABLE "notification" ADD FOREIGN KEY ("submission_id") REFERENCES "submission" ("submission_id");

ALTER TABLE "config" ADD FOREIGN KEY ("project_id") REFERENCES "project" ("project_id");
